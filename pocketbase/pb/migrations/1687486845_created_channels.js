migrate((db) => {
  const collection = new Collection({
    "id": "npexvd0q2dv8v8p",
    "created": "2023-06-23 02:20:45.202Z",
    "updated": "2023-06-23 02:20:45.202Z",
    "name": "channels",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "xdldypki",
        "name": "channel_id",
        "type": "number",
        "required": false,
        "unique": false,
        "options": {
          "min": null,
          "max": null
        }
      }
    ],
    "indexes": [],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("npexvd0q2dv8v8p");

  return dao.deleteCollection(collection);
})
