"""Simulation of Software FJ. Failed cases are logged and the run continues."""

from client import Client
from event_log import get_logger
from exceptions import SoftwareFJError
from registry import Registry
from services import EquipmentRental, RoomBooking, SpecializedConsulting


def run_case(number, title, action):
    log = get_logger()
    print(f"\n[{number}] {title}")
    try:
        result = action()
    except SoftwareFJError as error:
        cause = error.__cause__
        if cause is None:
            detail = str(error)
        else:
            detail = f"{error} | cause: {cause}"
        log.error("case %s failed: %s", number, detail)
        print(f"  controlled error: {detail}")
    else:
        log.info("case %s ok: %s", number, result)
        print(f"  ok: {result}")
    finally:
        print("  case closed, execution continues")


def main():
    company = Registry()
    saved = {}
    print("Software FJ - client, service and reservation simulation")

    def remember(key):
        def _store(value):
            saved[key] = value
            return value.describe()
        return _store

    run_case(
        1,
        "Register a valid client",
        lambda: remember("ana")(
            company.register_client(
                Client(
                    "C-001",
                    "Ana Maria Rojas",
                    "1020304050",
                    "ana.rojas@correo.com",
                    "3001112233",
                )
            )
        ),
    )
    run_case(
        2,
        "Reject a client with a broken email",
        lambda: Client(
            "C-002", "Pedro Alvarez", "1010101010", "pedro@", "3012223344"
        ).describe(),
    )
    run_case(
        3,
        "Reject a client without a document",
        lambda: Client(
            "C-003", "Luis Gomez", "", "luis.gomez@correo.com", "3023334455"
        ).describe(),
    )
    run_case(
        4,
        "Reject a duplicated document",
        lambda: company.register_client(
            Client(
                "C-004",
                "Ana Rojas copia",
                "1020304050",
                "ana.copia@correo.com",
                "3009998877",
            )
        ).describe(),
    )
    run_case(
        5,
        "Create a room booking service",
        lambda: remember("room")(
            company.add_service(RoomBooking("SALA-01", "Sala de juntas A", 80000))
        ),
    )
    run_case(
        6,
        "Reject equipment with a negative rate",
        lambda: EquipmentRental("EQ-01", "Portatil", -15000).describe(),
    )
    run_case(
        7,
        "Create a consulting service",
        lambda: remember("consulting")(
            company.add_service(
                SpecializedConsulting("CON-01", "Asesoria en bases de datos", 120000)
            )
        ),
    )
    run_case(
        8,
        "Create an equipment rental",
        lambda: remember("projector")(
            company.add_service(EquipmentRental("EQ-02", "Video beam", 20000, units=2))
        ),
    )
    run_case(
        9,
        "Register a room that is closed",
        lambda: remember("closed_room")(
            company.add_service(
                RoomBooking("SALA-02", "Sala de capacitacion", 90000, available=False)
            )
        ),
    )
    run_case(
        10,
        "Confirm a room reservation",
        lambda: _confirm(company, "R-001", saved["ana"], saved["room"], 2),
    )
    run_case(
        11,
        "Fail a reservation on an unavailable room",
        lambda: _confirm(company, "R-002", saved["ana"], saved["closed_room"], 3),
    )
    run_case(
        12,
        "Cancel a reservation and then try to cancel it again",
        lambda: _cancel_twice(company, saved["ana"], saved["projector"]),
    )
    run_case(
        13,
        "Reject a discount above 100 percent",
        lambda: saved["room"].calculate_cost_with_discount(2, 1.5),
    )
    run_case(
        14,
        "Reject a reservation with zero hours",
        lambda: company.create_reservation(
            "R-004", saved["ana"], saved["room"], 0
        ).describe(),
    )
    run_case(
        15,
        "Confirm and process a consulting reservation",
        lambda: _confirm_and_process(company, saved["ana"], saved["consulting"]),
    )
    run_case(
        16,
        "Reject processing a reservation that is still pending",
        lambda: company.create_reservation(
            "R-006", saved["ana"], saved["projector"], 4
        ).process(),
    )
    run_case(
        17,
        "Reject a consulting session longer than 8 hours",
        lambda: saved["consulting"].calculate_cost(10),
    )
    run_case(
        18,
        "Price the video beam with tax only",
        lambda: saved["projector"].calculate_cost_with_tax(3, 0.19),
    )

    print("\n--- what stayed in memory ---")
    for client in company.clients:
        print(" ", client.describe())
    for service in company.services:
        print(" ", service.describe())
    for reservation in company.reservations:
        print(" ", reservation.describe())
    print("\nLog written to logs/events.log")


def _confirm(company, code, client, service, hours):
    reservation = company.create_reservation(code, client, service, hours)
    total = reservation.confirm()
    return f"{reservation.describe()} -> confirmed total {total}"


def _cancel_twice(company, client, service):
    reservation = company.create_reservation("R-003", client, service, 2)
    reservation.confirm()
    reservation.cancel()
    reservation.cancel()
    return reservation.describe()


def _confirm_and_process(company, client, service):
    reservation = company.create_reservation("R-005", client, service, 3)
    reservation.confirm()
    total = reservation.process()
    return f"{reservation.describe()} -> processed total {total}"


if __name__ == "__main__":
    main()
