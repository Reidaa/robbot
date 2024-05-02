migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6mexouxnd1arbn1")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "o1ryvtfe",
    "name": "last_chapter",
    "type": "number",
    "required": true,
    "unique": false,
    "options": {
      "min": -1,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("6mexouxnd1arbn1")

  // update
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "o1ryvtfe",
    "name": "last_chapter",
    "type": "number",
    "required": false,
    "unique": false,
    "options": {
      "min": -1,
      "max": null
    }
  }))

  return dao.saveCollection(collection)
})
