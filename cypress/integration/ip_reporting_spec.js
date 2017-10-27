describe('IP reporting', function() {
  beforeEach(function() {
    cy.login()
    cy.visit('/api/admin')
  })

  it('click opens the PD section', function() {
    cy.visit('/app/BE/ip-reporting/overview', {timeout: 5000})
    cy.wait(5000)

    // this works
    cy.get('h1').should('contain', 'Overview')

    //this also works
    cy.get('a[href="/app/BE/ip-reporting/pd"]').should('contain', 'Programme')

    //this doesn't
    cy.get('a[href="/app/BE/ip-reporting/pd"]').click()
    cy.wait(5000)
  })
})