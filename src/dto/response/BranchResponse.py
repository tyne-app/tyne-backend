class BranchResponse:
    branch_id: int
    state_name: str
    state_id: int
    street: str
    street_number: str
    restaurant_name: str
    restaurant_description: str
    rating: int
    avg_price: int
    min_price: int
    max_price: int
    url_image: str

    def to_all_branch(self, client_id, branches):
        branches_response: list[BranchResponse] = []
        for branch in branches:
            branch_response = BranchResponse()

            if client_id:
                branch_response.avg_price = round(branch.avg_price)
                branch_response.min_price = branch.min_price
                branch_response.max_price = branch.max_price
                branch_response.rating = branch.rating

            branch_response.branch_id = branch.branch_id
            branch_response.state_name = branch.state_name
            branch_response.state_id = branch.state_id
            branch_response.street = branch.street
            branch_response.street_number = branch.street_number
            branch_response.restaurant_name = branch.restaurant_name
            branch_response.restaurant_description = branch.restaurant_description
            branch_response.url_image = branch.url_image

            branches_response.append(branch_response)
        return branches_response
