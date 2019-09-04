Routes related to users

[TODO]

Routes related to categories

|action |method(http)|path |function|
|-------|-------|-----|--------| 
|index  |get    |/categories|categoriesIndex|
|show   |get    |/categories/:id|categoriesShow|
|edit   |edit   |/categories/:id/edit|categoriesEdit|
|update |post   |/categories/:id/edit|categoriesUpdate|
|new    |get    |/categories/:id/new|categoriesNew|
|create  |post   |/categories|categoriesCreate|
|destroy  |post    |/categories/:id/delete|categoriesDestroy|

Routes related to Items

|action |method(http)|path |function|
|-------|-------|-----                            |--------| 
|index  |get    |/categories/:id/items            |Item|
|show   |get    |/categories/:id/items/:id        |categoriesShow|
|edit   |get    |/categories/:id/items/:id/edit   |categoriesEdit|
|update |post   |/categories/:id/items/:id/edit   |categoriesUpdate|
|new    |get    |/categories/:id/items/:id/new    |categoriesNew|
|create |post   |/categories/:id/items            |categoriesCreate|
|destroy|post   |/categories/:id/items/:id/delete |categoriesDestroy|
