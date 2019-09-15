Routes related to users

[TODO]

Routes related to categories

|action |method(http)|path |function|
|-------|-------|-----|--------| 
|index  |get    |/categories            |categoriesIndex|
|edit   |edit   |/categories/:id/edit   |categoriesEdit|
|update |post   |/categories/:id/edit   |categoriesUpdate|
|new    |get    |/categories/new    |categoriesNew|
|create |post   |/categories            |categoriesCreate|
|destroy|post   |/categories/:id/delete |categoriesDestroy|

Routes related to Items

|action |method(http)|path |function|
|-------|-------|-----                            |--------| 
|index  |get    |/categories/:id/items            |Items|
|show   |get    |/categories/:id/items/:id        |ItemsShow|
|edit   |get    |/categories/:id/items/:id/edit   |ItemsEdit|
|update |post   |/categories/:id/items/:id/edit   |ItemsUpdate|
|new    |get    |/categories/:id/items/new        |ItemsNew|
|create |post   |/categories/:id/items            |ItemsCreate|
|destroy|post   |/categories/:id/items/:id/delete |ItemsDestroy|
