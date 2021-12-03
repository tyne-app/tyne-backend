from repository.entity.CategoryEntity import CategoryEntity


class CategoryResponse:
    id: str
    name: str

    def to_all_categories(self, categories: list[CategoryEntity]):
        categories_response: list[CategoryResponse] = []
        for category in categories:
            category_response = CategoryResponse()
            category_response.id = category.id
            category_response.name = category.name
            categories_response.append(category_response)
        return categories_response
