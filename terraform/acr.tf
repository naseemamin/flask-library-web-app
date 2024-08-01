resource "azurerm_container_registry" "flasklibrarywebapp" {
  name                = "flasklibrarywebapp"
  resource_group_name = azurerm_resource_group.flask-app.name
  location            = azurerm_resource_group.flask-app.location
  sku                 = "Basic"
  admin_enabled       = true
  tags                = {environment = "development"}
}