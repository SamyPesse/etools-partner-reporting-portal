describe("Cluster reporting", function() {
  let workspace, responsePlan1, responsePlan2
  before(function() {
    //TODO change this to creating test IMO user and logging in as him in beforeEach blocks
  })
  beforeEach(function() {
    cy.login()
    Cypress.Cookies.preserveOnce('csrftoken')
    cy.visit('/api/admin')
  })
  after(function() {
    //TODO delete created test IMO user

    // this deletes the workspace and everything that was associated with it
    cy.delete(`/api/admin/core/workspace/${workspace}/delete/`)
  })
  describe('Logged in IMO', function() {
    

    it('creates a new workspace', function() {
      cy.get('a[href="/api/admin/core/workspace/add/"]').click()
      cy.get('input[name=title]').type('test_workspace')
      cy.get('input[name=workspace_code]').type('testcode')
      cy.get('select[name=countries]').select('1')
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
      cy.get('li[class=success]>a')
        .then(($element) => {
          let href = $element.attr('href').split('/')
          workspace = href[href.length-3]
        })
    })

    it('creates a new response plan', function() {
      cy.get('a[href="/api/admin/core/responseplan/add/"]').click()
      cy.get('input[name=title]').type('test_response_plan1')
      cy.get('select[name=workspace]').select(workspace)
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
      cy.get('li[class=success]>a')
        .then(($element) => {
          let href = $element.attr('href').split('/')
          responsePlan1 = href[href.length-3]
        })
    })

    it('creates another new response plan', function() {
      cy.get('a[href="/api/admin/core/responseplan/add/"]').click()
      cy.get('input[name=title]').type('test_response_plan2')
      cy.get('select[name=workspace]').select(workspace)
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
      cy.get('li[class=success]>a')
        .then(($element) => {
          let href = $element.attr('href').split('/')
          responsePlan2 = href[href.length-3]
        })
    })

    it('creates a new cluster', function() {
      cy.get('a[href="/api/admin/cluster/cluster/add/"]').click()
      cy.get('select[name=type]').select('cccm')
      cy.get('select[name=response_plan]').select(responsePlan1)
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
    })

    it('creates another new cluster', function() {
      cy.get('a[href="/api/admin/cluster/cluster/add/"]').click()
      cy.get('select[name=type]').select('cccm')
      cy.get('select[name=response_plan]').select(responsePlan2)
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
    })

    it('creates one more new cluster', function() {
      cy.get('a[href="/api/admin/cluster/cluster/add/"]').click()
      cy.get('select[name=type]').select('wash')
      cy.get('select[name=response_plan]').select(responsePlan1)
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
    })

    it('creates one more new cluster', function() {
      cy.get('a[href="/api/admin/cluster/cluster/add/"]').click()
      cy.get('select[name=type]').select('wash')
      cy.get('select[name=response_plan]').select(responsePlan2)
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
    })
  })
})