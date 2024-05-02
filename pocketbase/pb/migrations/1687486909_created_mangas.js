migrate((db) => {
  const collection = new Collection({
    "id": "6mexouxnd1arbn1",
    "created": "2023-06-23 02:21:49.034Z",
    "updated": "2023-06-23 02:21:49.034Z",
    "name": "mangas",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "g2vhhvn6",
        "name": "name",
        "type": "text",
        "required": true,
        "unique": false,
        "options": {
          "min": null,
          "max": null,
          "pattern": ""
        }
      },
      {
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
      },
      {
        "system": false,
        "id": "arkuuxyl",
        "name": "cover_url",
        "type": "url",
        "required": false,
        "unique": false,
        "options": {
          "exceptDomains": null,
          "onlyDomains": null
        }
      }
    ],
    "indexes": [
      "CREATE UNIQUE INDEX `idx_Q5xRfA4` ON `mangas` (`name`)"
    ],
    "listRule": "",
    "viewRule": "",
    "createRule": "",
    "updateRule": "",
    "deleteRule": "",
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("6mexouxnd1arbn1");

  return dao.deleteCollection(collection);
})
