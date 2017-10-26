// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

//TODO make this first seed the user, only then login
Cypress.Commands.add('login', function(token=null) {
  let csrf;
  cy.request('/api/admin/login/')
    .its('body')
    .then((body) => {
      if (token) {
        csrf = token
      } else {
        // we can use Cypress.$ to parse the string body
        // thus enabling us to query into it easily
        const $html = Cypress.$(body)
        csrf  = $html.find("input[name=csrfmiddlewaretoken]").val()
      }
      cy.request({
        method: 'POST',
        url: '/api/admin/login/?next=/api/admin/',
        failOnStatusCode: false, // dont fail so we can make assertions
        form: true, // we are submitting a regular form body
        body: {
          username: 'admin_ao',
          password: 'Passw0rd!',
          csrfmiddlewaretoken: csrf // insert this as part of form body
        }
      })
        
    })
  })

Cypress.Commands.add('delete', function(url) {
  cy.visit(url)
  cy.get("input[type=submit]").click()
})
