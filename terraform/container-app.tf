# resource "azurerm_container_app_environment" "flask-app-env" {
#   name                       = "flask-app-env"
#   location                   = azurerm_resource_group.flask-app.location
#   resource_group_name        = azurerm_resource_group.flask-app.name
# }


# resource "azurerm_container_app" "flasklibrarywebapp" {
#   name                         = "flasklibrarywebapp"
#   container_app_environment_id = azurerm_container_app_environment.flask-app-env.id
#   resource_group_name          = azurerm_resource_group.flask-app.name
#   revision_mode                = "Single"

#   template {
#     container {
#       name   = "flasklibrarywebapp"
#       image  = format("%s/flasklibrarywebapp:0.0.0",azurerm_container_registry.flasklibrarywebapp.login_server)
#       cpu    = 0.25
#       memory = "0.5Gi"
#     }
#   }
# }