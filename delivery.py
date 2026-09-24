import random
from urllib.parse import urljoin
import requests


from headers import headers
from faker import Faker

from model_get_delivery import Get_Delivery
from model_get_package_item import Get_Package_Item
from model_sendback_response import Sendback_Adapter


LOG_ENABLED = True
LOG_FILENAME = "log.txt"
BASE_URL = "http://best-delivery-processor.lostfound.ru"

fake = Faker("ru_RU")

customer_id = random.randrange(100000000)

rack_id = 241515
rack_space_id = 156261551
package_class_id = 2678362
price = 1000
commission = 0
total = price + commission

customer_first_name = fake.first_name_male()
customer_last_name = fake.last_name_male()
customer_email = fake.email()
customer_phone = fake.phone_number()

client_first_name = fake.first_name_male()
client_last_name = fake.last_name_male()
client_email = fake.email()
client_phone = fake.phone_number()

doc_enum = [
    "DRIVERS_LICENSE",
    "PASSPORT",
    "NATIONAL_ID_CARD",
    "BIRTH_CERTIFICATE",
    "MARRIAGE_CERTIFICATE",
    "UTILITY_BILL",
    "BANK_STATEMENT",
    "TAX_RETURN",
    "SOCIAL_SECURITY_CARD",
    "MILITARY_ID",
    "HEALTH_INSURANCE_CARD",
    "STUDENT_ID",
    "RESIDENCE_PERMIT",
    "VOTER_REGISTRATION_CARD",
    "EMPLOYMENT_CONTRACT",
    "VEHICLE_REGISTRATION",
    "LAND_DEED",
    "DIPLOMA_CERTIFICATE",
    "MEDICAL_RECORD",
    "POWER_OF_ATTORNEY",
]

client_document = random.choice(doc_enum)


def func_get_delivery(delivery_id: int) -> Get_Delivery:
    """Delivery info"""
    response = requests.get(
        urljoin(BASE_URL, f"/api-new/v4/deliverys/{delivery_id}"),
        headers=headers,
    )

    write_log(
        [
            response.status_code,
            response.url,
            response.text,
        ]
    )

    response.raise_for_status()
    get_delivery = Get_Delivery.model_validate_json(json_data=response.content)
    print("Get delivery validation complete")
    return get_delivery


def func_get_package_item(package_item_id: int) -> Get_Package_Item:
    """Package item info"""
    response = requests.get(
        urljoin(BASE_URL, f"/api-new/v4/tickets/{package_item_id}"),
        headers=headers,
    )

    write_log(
        [
            response.status_code,
            response.url,
            response.text,
        ]
    )

    response.raise_for_status()
    get_package_item = Get_Package_Item.model_validate_json(json_data=response.content)
    print("Get package item validation complete")
    return get_package_item


def func_get_refund_terms(ticket_id: int) -> Sendback_Adapter:
    """Send back info"""
    response = requests.get(
        urljoin(BASE_URL, f"/api-new/v4/tickets/refund-terms?id={ticket_id}"),
        headers=headers,
    )

    write_log(
        [
            response.status_code,
            response.url,
            response.text,
        ]
    )

    response.raise_for_status()
    refund_terms = Sendback_Adapter.validate_json(
        response.content
    )  # done differently !!!
    print("Send back terms validation complete")
    return Sendback_Adapter


def func_create_delivery(
    customer_id: int,
    rack_id: int,
    rack_space_id: int,
    package_class_id: int,
    price: int,
    commission: int,
    customer_first_name: str,
    customer_last_name: str,
    customer_phone: str,
    customer_email: str,
    client_first_name: str,
    client_last_name: str,
    client_phone: str,
    client_email: str,
    client_document: str,
) -> Get_Delivery:
    """Creates delivery"""
    response = requests.post(
        urljoin(BASE_URL, "/api-new/v4/deliverys/"),
        headers=headers,
        json={
            "customerInfo": {
                "id": customer_id,
                "surname": customer_last_name,
                "name": customer_first_name,
                "middlename": "",
                "phone": customer_phone,
                "email": customer_email,
            },
            "places": [
                {
                    "rack_id": rack_id,
                    "rack_space_id": rack_space_id,
                    "package_class_id": package_class_id,
                    "price": price,
                    "commission": commission,
                    "clientInfo": {
                        "surname": client_last_name,
                        "name": client_first_name,
                        "middlename": "",
                        "phonenumber": client_phone,
                        "email": client_email,
                        "documentType": client_document,
                        "documentSeries": "fbw151561",
                        "documentNumber": "vsf245151",
                        "destinationPoint": "vaf12425",
                    },
                }
            ],
        },
    )

    write_log(
        [
            response.status_code,
            response.url,
            response.text,
        ]
    )

    print()
    print(response.content)
    print()

    response.raise_for_status()
    reply = Get_Delivery.model_validate_json(json_data=response.content)
    print("Delivery created, delivery validation complete")

    # print(delivery.model_dump_json(indent=2))
    print("deliveryId:", reply.id)

    return reply.id


def func_delivery_pay(
    delivery_id: int,
    total: int,
) -> Get_Delivery:
    """Paying for the Delivery"""
    response = requests.post(
        urljoin(BASE_URL, f"/api-new/v4/deliveries/{delivery_id}/payments"),
        headers=headers,
        json={
            "payments": [
                {
                    "payment_type": "CREDIT_CARD",
                    "transaction_id": "abcdefg123456",
                    "general_rrn": "123456789",
                    "general_provider": "MEGABANK",
                    "sum": total,
                }
            ]
        },
    )

    write_log(
        [
            response.status_code,
            response.url,
            response.text,
        ]
    )

    response.raise_for_status()
    reply = Get_Delivery.model_validate_json(json_data=response.content)
    print("Delivery is paid for, payment validation complete")

    # print(delivery.model_dump_json(indent=2))
    print("Delivery item id:", reply.places[0].packageItem.packageItemId)

    return reply.places[0].packageItem.packageItemId


def func_return_delivery_items(
    delivery_id: int,
    package_item_id: int,
    price: int,
):
    """Return delivery items, refund money, cancel delivery"""
    response = requests.post(
        urljoin(BASE_URL, f"/api-new/v4/deliveries/{delivery_id}/items/delete"),
        headers=headers,
        json={
            "packageItems": [
                {
                    "package_item_id": package_item_id,
                    "refund_reason": "SUPPLY_CHAIN_ISSUE",
                    "refundSum": price,
                }
            ]
        },
    )

    write_log(
        [
            response.status_code,
            response.url,
            response.text,
        ]
    )

    response.raise_for_status()

    print("Delivery is successfully returned. No validation, required")

    return None


def func_cancel_delivery(delivery_id: int):
    """Cancel unpaid delivery"""
    response = requests.delete(
        urljoin(BASE_URL, f"/api-new/v4/deliveries/{delivery_id}"),
        headers=headers,
    )

    write_log(
        [
            response.status_code,
            response.url,
            response.text,
        ]
    )

    response.raise_for_status()
    print("Unpaid delivery successfully cancelled")
    return None


def write_log(data: list[str]) -> None:
    """Saving logs to a file"""
    if not LOG_ENABLED:
        return

    with open(LOG_FILENAME, "a", encoding="utf-8") as file:
        for line in data:
            file.write(str(line))
            file.write(" ")
        file.write("\n\n")


def main():

    delivery_id_1 = func_create_delivery(
        customer_id,
        rack_id,
        rack_space_id,
        package_class_id,
        price,
        commission,
        customer_first_name,
        customer_last_name,
        customer_phone,
        customer_email,
        client_first_name,
        client_last_name,
        client_phone,
        client_email,
        client_document,
    )

    func_get_delivery(delivery_id_1)
    package_item_id = func_delivery_pay(delivery_id_1, total)
    func_get_package_item(package_item_id)
    func_get_refund_terms(package_item_id)
    func_return_delivery_items(delivery_id_1, package_item_id, price)

    delivery_id_2 = func_create_delivery(
        customer_id,
        rack_id,
        rack_space_id,
        package_class_id,
        price,
        commission,
        customer_first_name,
        customer_last_name,
        customer_phone,
        customer_email,
        client_first_name,
        client_last_name,
        client_phone,
        client_email,
        client_document,
    )

    func_cancel_delivery(delivery_id_2)
    func_get_delivery(delivery_id_2)


if __name__ == "__main__":
    main()
