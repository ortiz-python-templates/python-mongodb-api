const views = db.getCollectionInfos({ type: "view" });

views.forEach(view => {
    print("Removendo view:", view.name);
    db[view.name].drop();
});


