migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6mexouxnd1arbn1")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "xch2vdqn",
    "name": "channels",
    "type": "relation",
    "required": false,
    "unique": false,
    "options": {
      "collectionId": "viyn8674i5glpcj",
      "cascadeDelete": false,
      "minSelect": null,
      "maxSelect": null,
      "displayFields": []
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6mexouxnd1arbn1")

  // remove
  collection.schema.removeField("xch2vdqn")

  return dao.saveCollection(collection)
})
