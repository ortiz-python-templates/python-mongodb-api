db.getCollectionInfos().forEach(info => {
    if (info.type === "collection" && !info.name.startsWith("system.")) {
        db[info.name].dropIndexes();
    }
});
