from redis_om import JsonModel


class GetCompanyDetailsResource(JsonModel):
    user_id: str