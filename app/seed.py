from app.store import DataStore
from app.models.document import DocumentCreate

# (document, days since last review)
SEED_DOCUMENTS = [
    (DocumentCreate(
        title="Fryer Oil Change and Filtration SOP",
        category="SOP",
        owner_id=1,
        body=(
            "Fryer oil must be filtered every night after service and fully replaced every "
            "three days, or sooner if the oil is dark, foams, or smells rancid. Before "
            "draining, turn the fryer off and let the oil cool to 100 degrees Fahrenheit. "
            "Never drain hot oil. Drain into the approved oil transport container, wipe the "
            "vat clean, and refill to the fill line. Log every filtration and change on the "
            "fryer maintenance sheet with your initials and the time."
        ),
    ), 5),
    (DocumentCreate(
        title="Knife Sharpening and Storage SOP",
        category="SOP",
        owner_id=4,
        body=(
            "Knives are honed at the start of every shift and sharpened on the whetstone every "
            "Monday by the Prep lead. A dull knife is a safety hazard because it slips. Never "
            "leave knives in a sink or soak them. After washing, dry each knife and return it "
            "to the magnetic strip or the labeled knife roll. Report any chipped or bent blade "
            "to the sous chef immediately and take it out of service."
        ),
    ), 20),
    (DocumentCreate(
        title="Walk-in Cooler Temperature SOP",
        category="SOP",
        owner_id=5,
        body=(
            "The walk-in cooler must be kept at 41 degrees Fahrenheit or below at all times. "
            "Check and log the temperature at the start of each shift and again at midday. "
            "If the reading is above 41 degrees, tell the sous chef right away, check that "
            "the door is sealing, and move high-risk items such as raw poultry and dairy to a "
            "working cooler. Any food that has been above 41 degrees for more than four hours "
            "must be discarded and recorded on the waste log."
        ),
    ), 10),
    (DocumentCreate(
        title="Classic Creme Brulee Recipe",
        category="Recipe",
        owner_id=3,
        body=(
            "Yields twelve ramekins. Heat four cups of heavy cream with one vanilla bean until "
            "steaming but not boiling. Whisk eight egg yolks with three quarters of a cup of "
            "sugar until pale. Slowly temper the hot cream into the yolks, then strain. Pour "
            "into ramekins set in a water bath and bake at 325 degrees Fahrenheit for 35 to 40 "
            "minutes, until the edges are set and the center still jiggles slightly. Chill for "
            "at least four hours. Sugar and torch the tops just before serving."
        ),
    ), 30),
    (DocumentCreate(
        title="New Line Cook Onboarding Guide",
        category="Onboarding",
        owner_id=2,
        body=(
            "Welcome to Hearthline. Arrive fifteen minutes before your shift in a clean "
            "uniform and non-slip shoes. Wash your hands when you arrive and after handling "
            "raw proteins. Your first week is spent shadowing your station lead. Ask before "
            "using any equipment you have not been trained on. Recipes and prep guides are "
            "kept at each station, and food-safety SOPs are posted by the hand sink. If you "
            "are unsure about anything, ask your station lead before guessing."
        ),
    ), 45),
    (DocumentCreate(
        title="Grill Station Opening Checklist",
        category="SOP",
        owner_id=2,
        body=(
            "Scrape and oil the grill grates. Check the gas line and confirm the pilot lights "
            "are lit. Bring the grill to full temperature about twenty minutes before service. "
            "Stock the station with tongs, spatulas, and side towels. Confirm the proteins for "
            "the day have been pulled from the walk-in and are held at 41 degrees or below "
            "until they go on the grill."
        ),
    ), 130),  # stale on purpose
    (DocumentCreate(
        title="Incident Report: Walk-in Cooler Failure",
        category="Incident Report",
        owner_id=5,
        body=(
            "The walk-in cooler compressor failed overnight and the temperature reached 52 "
            "degrees Fahrenheit before the opening cook noticed. Roughly two hundred pounds of "
            "raw chicken, dairy, and prepped vegetables were discarded. The morning log had "
            "not been completed the previous evening. Follow-up: temperature checks are now "
            "required at the start of each shift and at midday, and a maintenance contact was "
            "added to the cooler door."
        ),
    ), 200),  # old, but Incident Reports are excluded from the stale check
]


def seed_documents(store: DataStore) -> None:
    from datetime import datetime, UTC, timedelta
    for data, days_old in SEED_DOCUMENTS:
        doc = store.create_document(data)
        if days_old:
            doc.last_reviewed_at = datetime.now(UTC) - timedelta(days=days_old)