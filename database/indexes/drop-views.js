const views = db.getCollectionInfos({ type: "view" });

views.forEach(view => {
    print("Removing view:", view.name);
    db[view.name].drop();
});


