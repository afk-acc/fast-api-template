



async def get_list_data(model, page: int, limit: int):
    return {
        'data': await model.paginate(page=page, limit=limit),
        'total': await model.count(),
        'page': page,
        'limit': limit
    }
