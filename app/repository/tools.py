



async def get_list_data(model, page: int, limit: int, filter=None):
    return {
        'data': await model.paginate(page=page, limit=limit, filter=filter),
        'total': await model.count(filter=filter),
        'page': page,
        'limit': limit
    }
