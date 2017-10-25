describe('General Actions', function() {

  describe('Login to django admin with UI', function() {

    after(function() {
      cy.visit('/api/admin/logout/').get('body').contains('Logged out')
    })

    it('it logs in the user to django admin', function() {
      cy.visit('/api/admin')
      cy.get('input[name=username]').type('admin_ao')
      cy.get('input[name=password]').type('Passw0rd!{enter}')
      cy.get('#user-tools').contains('admin_ao')
    })
    
  })

  describe('Logging In to django admin without UI', function(){

    it('403 status without a valid CSRF token', function(){
      // first show that by not providing a valid CSRF token
      // that we will get a 403 status code
      cy.login('invalid-token')
        .its('status')
        .should('eq', 403)
    })

    it('parses token from HTML and logins successfully', function(){
      cy.request('/api/admin/login/')
        .its('body')
        .then((body) => {
          // we can use Cypress.$ to parse the string body
          // thus enabling us to query into it easily
          const $html = Cypress.$(body)
          const csrf  = $html.find("input[name=csrfmiddlewaretoken]").val()
          cy.login(csrf)
            .then((resp) => {
              expect(resp.status).to.eq(200)
            })
        })
    })
  })

  describe('Create different type of users', function() {
    
    beforeEach(function() {
      cy.login()
      cy.visit('/api/admin')
    })

    describe('successfully creates various users', function() {

      afterEach(function() {
        cy.get('table tbody tr').first().find('input[type=checkbox]').check()
        cy.get('select[name=action]').select('delete_selected')
        cy.get('button[type=submit]').click()
        cy.get('input[type=submit]').click()
        cy.get('li[class=success]').contains('Successfully deleted')
    })

      it('creates new IMO user', function() {
        cy.get('a[href="/api/admin/account/user/add/"]').click()
        cy.get('select[name=groups]').select('1')
        cy.get('input[name=username]').type('test_imo_user')
        cy.get('input[name=first_name]').type('test_imo_firstname')
        cy.get('input[name=last_name]').type('test_imo_lastname')
        cy.get('input[name=organization]').type('test_imo_organization')
        cy.get('input[name=email]').type('test_imo_user@email.com')
        cy.get('select[name=workspaces]').select('1')
        cy.get('select[name=imo_clusters').select('1')
        cy.get('input[name=_save]').click()
        cy.get('li[class=success]').contains('successfully')
      })

      it('creates new IP viewer', function() {
        cy.get('a[href="/api/admin/account/user/add/"]').click()
        cy.get('select[name=groups]').select('4')
        cy.get('input[name=username]').type('test_ipViewer_user')
        cy.get('input[name=first_name]').type('test_ipViewer_firstname')
        cy.get('input[name=last_name]').type('test_ipViewer_lastname')
        cy.get('input[name=organization]').type('test_ipViewer_organization')
        cy.get('input[name=email]').type('test_ipViewer_user@email.com')
        cy.get('select[name=partner]').select('1')
        cy.get('select[name=workspaces]').select('1')
        cy.get('input[name=_save]').click()
        cy.get('li[class=success]').contains('successfully')
      })

      it('creates new IP editor', function() {
        cy.get('a[href="/api/admin/account/user/add/"]').click()
        cy.get('select[name=groups]').select('3')
        cy.get('input[name=username]').type('test_ipEditor_user')
        cy.get('input[name=first_name]').type('test_ipEditor_firstname')
        cy.get('input[name=last_name]').type('test_ipEditor_lastname')
        cy.get('input[name=organization]').type('test_ipEditor_organization')
        cy.get('input[name=email]').type('test_ipEditor_user@email.com')
        cy.get('select[name=partner]').select('1')
        cy.get('select[name=workspaces]').select('1')
        cy.get('input[name=_save]').click()
        cy.get('li[class=success]').contains('successfully')
      })

      it('creates new IP Authorized officer', function() {
        cy.get('a[href="/api/admin/account/user/add/"]').click()
        cy.get('select[name=groups]').select('2')
        cy.get('input[name=username]').type('test_ipOfficer_user')
        cy.get('input[name=first_name]').type('test_ipOfficer_firstname')
        cy.get('input[name=last_name]').type('test_ipOfficer_lastname')
        cy.get('input[name=organization]').type('test_ipOfficer_organization')
        cy.get('input[name=email]').type('test_ipOfficer_user@email.com')
        cy.get('select[name=partner]').select('1')
        cy.get('select[name=workspaces]').select('1')
        cy.get('input[name=_save]').click()
        cy.get('li[class=success]').contains('successfully')
      })
    })

    describe('Gives an error if some required field is empty', function() {

      afterEach(function() {
        cy.visit('/api/admin')
      })

      it('gives an error if creating a new IMO user no imo clusters are selected', function() {
        cy.get('a[href="/api/admin/account/user/add/"]').click()
        cy.get('select[name=groups]').select('1')
        cy.get('input[name=username]').type('test_imo_user')
        cy.get('input[name=first_name]').type('test_imo_firstname')
        cy.get('input[name=last_name]').type('test_imo_lastname')
        cy.get('input[name=organization]').type('test_imo_organization')
        cy.get('input[name=email]').type('test_imo_user@email.com')
        cy.get('select[name=workspaces]').select('1')
        cy.get('input[name=_save]').click()
        cy.get('li').contains('Please select one or more IMO clusters.')
      })

      it('gives an error if creating a new IP viewer no partner is selected', function() {
        cy.get('a[href="/api/admin/account/user/add/"]').click()
        cy.get('select[name=groups]').select('4')
        cy.get('input[name=username]').type('test_ipViewer_user')
        cy.get('input[name=first_name]').type('test_ipViewer_firstname')
        cy.get('input[name=last_name]').type('test_ipViewer_lastname')
        cy.get('input[name=organization]').type('test_ipViewer_organization')
        cy.get('input[name=email]').type('test_ipViewer_user@email.com')
        cy.get('select[name=workspaces]').select('1')
        cy.get('input[name=_save]').click()
        cy.get('li').contains('Please select a partner for this user.')
      })

      it('gives an error if creating a new IP editor no partner is selected', function() {
        cy.get('a[href="/api/admin/account/user/add/"]').click()
        cy.get('select[name=groups]').select('3')
        cy.get('input[name=username]').type('test_ipEditor_user')
        cy.get('input[name=first_name]').type('test_ipEditor_firstname')
        cy.get('input[name=last_name]').type('test_ipEditor_lastname')
        cy.get('input[name=organization]').type('test_ipEditor_organization')
        cy.get('input[name=email]').type('test_ipEditor_user@email.com')
        cy.get('select[name=workspaces]').select('1')
        cy.get('input[name=_save]').click()
        cy.get('li').contains('Please select a partner for this user.')
      })

      it('gives an error if creating a new IP Authorized officer no partner is selected', function() {
        cy.get('a[href="/api/admin/account/user/add/"]').click()
        cy.get('select[name=groups]').select('2')
        cy.get('input[name=username]').type('test_ipEditor_user')
        cy.get('input[name=first_name]').type('test_ipEditor_firstname')
        cy.get('input[name=last_name]').type('test_ipEditor_lastname')
        cy.get('input[name=organization]').type('test_ipEditor_organization')
        cy.get('input[name=email]').type('test_ipEditor_user@email.com')
        cy.get('select[name=workspaces]').select('1')
        cy.get('input[name=_save]').click()
        cy.get('li').contains('Please select a partner for this user.')
      })

    })

  })
})
