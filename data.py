from faker import Faker

faker = Faker()


def get_register():
    return {
        "name": faker.name,
        "address": faker.address,
        "created_at": faker
    }
