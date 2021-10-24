class SearchDAO:

    def search_local(raw_query: str, db: Session):
        try:
            all_branch = db.execute(raw_query)
            preview_branch_list = []
            for branch in all_branch:
                preview_branch_list.append(dict(branch))
            db.close()
            return preview_branch_list
        except Exception as error:
            return error.args[0]


    def read_branch(branch_id: int, db: Session):
        logger.info('branch_id: {}', branch_id)

        try:
            # TODO: Se puede refactorizar los pasos mezclando queries.
            # TODO: Falta caso uso cuando no hay datos para todos o ciertas queries.
            attributes_dict = {}
            # TODO: 1.- Query Branch listo.
            branch = db.query(
                Branch.id, Branch.description, Branch.latitude, Branch.longitude,
                Branch.accept_pet, Branch.street, Branch.street_number, Branch.restaurant_id, Restaurant.name)\
                .select_from(Branch).join(Restaurant, Restaurant.id == Branch.restaurant_id)\
                .filter(Branch.id == branch_id).filter(Branch.state).first()

            if not branch:
                return []

            attributes_dict['branch'] = branch

            # TODO: 2.- Query datos calculados

            aggregate_values = db.query(
                func.avg(Opinion.qualification).label("rating"),
                func.avg(Price.amount).label("price"),
                func.max(Price.amount).label("max_price"),
                func.min(Price.amount).label("min_price")
            ) \
                .select_from(Branch) \
                .join(Opinion, Opinion.branch_id == Branch.id) \
                .join(Product, Product.branch_id == Branch.id) \
                .join(Price, Price.product_id == Product.id) \
                .filter(Branch.id == branch_id) \
                .group_by(Branch.id) \
                .first()
            attributes_dict['aggregate_values'] = aggregate_values

            # TODO: 3.- Query schedule

            schedule_branch = db.query(Schedule).join(BranchSchedule, BranchSchedule.schedule_id == Schedule.id)\
                .join(Branch, Branch.id == BranchSchedule.branch_id).all()
            attributes_dict['schedule_branch'] = schedule_branch
            # TODO: 4.- Query branch del mismo restaurant.

            related_branch = db.query(Branch.id, Restaurant.name) \
                .select_from(Branch).join(Restaurant, Restaurant.id == Branch.restaurant_id)\
                .filter(Branch.restaurant_id == branch.restaurant_id) \
                .filter(Branch.id != branch.id).all()

            attributes_dict['related_branch'] = related_branch
            # TODO: 5.- Query Obtener todas las imagenes del branch. DEVUELVE UNA LISTA.

            branch_images = db.query(Image.id, Image.url) \
                .select_from(BranchImage) \
                .join(Image, Image.id == BranchImage.image_id) \
                .filter(BranchImage.branch_id == branch_id).all()
            attributes_dict['branch_images'] = branch_images
            # TODO: 6.- Query todas las opiniones de forma descendente segun branch.

            opinion_list = db.query(
                Opinion.id, Opinion.description, Opinion.qualification, Opinion.creation_date, Client.name, Client.last_name
            ) \
                .select_from(Opinion) \
                .join(Client, Client.id == Opinion.client_id) \
                .filter(Opinion.branch_id == branch_id) \
                .all()
            attributes_dict['opinion_list'] = opinion_list
            db.close()
            return attributes_dict
        except Exception as error:
            logger.error('error: {}', error)
            logger.error('error.args: {}', error.args)
            return error.args[0]
