from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    choosing_role = State()
    entering_full_name = State()
    entering_phone = State()
    entering_extra_phones = State()
    entering_org_name = State()
    entering_org_addresses = State()
    confirming = State()

class DentistMenuStates(StatesGroup):
    main_menu = State()
    new_order = State()
    view_orders = State()
    labs = State()
    settings = State()
    feedback = State()
    add_technician = State()
    request_collaboration = State()
    search_order = State()

class OrderFSM(StatesGroup):
    choose_lab = State()
    choose_location_type = State()
    choose_construction_type = State()
    choose_teeth = State()
    choose_material = State()
    choose_color = State()
    upload_files = State()
    add_comment = State()
    preview = State()
    confirm = State()

class TechnicianMenuStates(StatesGroup):
    main_menu = State()
    view_orders = State()
    dentists = State()
    settings = State()
    feedback = State()
    accept_order = State()
    decline_order = State()
    comment = State()
    finish_work = State()
