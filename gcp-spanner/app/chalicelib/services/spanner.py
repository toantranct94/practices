from typing import List

from google.cloud import spanner
from google.oauth2 import service_account as account
import uuid


class SpannerService():
    def __init__(
        self,
        instance_id: str,
        database_id: str,
        credentials_path: str,
    ) -> None:
        credentials = account.Credentials.from_service_account_file(
            credentials_path)
        self.spanner_client = spanner.Client(credentials=credentials)
        self.instance = self.spanner_client.instance(instance_id)
        self.database = self.instance.database(database_id)

    def get(self, singerid: str) -> List:

        params = {'p1': singerid}
        param_types = {'p1': spanner.param_types.INT64}

        with self.database.snapshot() as snapshot:
            result_set = snapshot.execute_sql(
                """
                    SELECT *
                    FROM singers
                    WHERE singerid = $1
                """,
                params=params,
                param_types=param_types)
            singer = result_set.one()
            return singer

    def all(self) -> List:
        with self.database.snapshot() as snapshot:
            result_set = snapshot.execute_sql("SELECT * FROM singers")
            results = list(result_set)
            return results

    def update_or_create(self, data: dict) -> bool:
        with self.database.batch() as batch:
            batch.insert_or_update(
                table="singers",
                columns=(
                    "singerid", "firstname",
                    "lastname", "birthdate", "singerinfo"
                ),
                values=[
                    (
                        data.pop("singerid", str(uuid.uuid4())),
                        data.pop("firstname"),
                        data.pop("lastname"),
                        data.pop("birthdate"),
                        data.pop("singerinfo")
                    )
                ],
            )
            return {
                "message": "Successfully"
            }

    def delete(self, id: str) -> bool:
        item_to_delete = spanner.KeySet(keys=[[id]])
        with self.database.batch() as batch:
            batch.delete("singers", item_to_delete)
        return {
            "message": "Deleted"
        }
