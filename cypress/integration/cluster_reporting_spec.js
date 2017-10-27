describe("Cluster reporting", function() {
  let workspace, responsePlan1, responsePlan2, cluster
  let partner
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
    cy.delete(`/api/admin/partner/partner/${partner}/delete/`)
  })

  describe('Logged in IMO in django admin', function() {
    
    //it's a one long test case because creating all these things depend on previously created things and we don't want
    // to make separate test cases for them to avoid close coupling
    it('creates a new workspace, response plans for that workspace and clusters for the response plans', function() {
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
        .then(() => {
          cy.visit('/api/admin')
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
            .then(() => {
              cy.visit('/api/admin')
              cy.get('a[href="/api/admin/cluster/cluster/add/"]').click()
              cy.get('select[name=type]').select('cccm')
              cy.get('select[name=response_plan]').select(responsePlan1)
              cy.get('input[name=_save]').click()
              cy.get('li[class=success]').contains('successfully')
              cy.get('li[class=success]>a')
                .then(($element) => {
                  let href = $element.attr('href').split('/')
                  cluster = href[href.length-3]
                })
              cy.visit('/api/admin')
              cy.get('a[href="/api/admin/cluster/cluster/add/"]').click()
              cy.get('select[name=type]').select('wash')
              cy.get('select[name=response_plan]').select(responsePlan1)
              cy.get('input[name=_save]').click()
              cy.get('li[class=success]').contains('successfully')
            })
          cy.visit('/api/admin')
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
            .then(() => {
              cy.visit('/api/admin')
              cy.get('a[href="/api/admin/cluster/cluster/add/"]').click()
              cy.get('select[name=type]').select('cccm')
              cy.get('select[name=response_plan]').select(responsePlan2)
              cy.get('input[name=_save]').click()
              cy.get('li[class=success]').contains('successfully')
              cy.visit('/api/admin')
              cy.get('a[href="/api/admin/cluster/cluster/add/"]').click()
              cy.get('select[name=type]').select('wash')
              cy.get('select[name=response_plan]').select(responsePlan2)
              cy.get('input[name=_save]').click()
              cy.get('li[class=success]').contains('successfully')
            })
          })
          
    })
    
  })

  describe('Logged to django admin user', function() {
    //not very good because it depends on previous test case that the cluster exists
    //ideally create seed db before this test case
    it('creates a new partner and associates it with cluster', function() {
      cy.get('a[href="/api/admin/partner/partner/add/"]').click()
      cy.get('input[name=title]').type('test_partner')
      cy.get('input[name=rating]').type('test_rating')
      cy.get('input[name=type_of_assessment]').type('test_assessment')
      cy.get('select[name=clusters]').select(cluster)
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
      cy.get('li[class=success]>a')
        .then(($element) => {
          let href = $element.attr('href').split('/')
          partner = href[href.length-3]
        })
    })

    it('creates a new user and associates it with partner', function() {
      cy.get('a[href="/api/admin/account/user/add/"]').click()
      cy.get('select[name=groups]').select('4')
      cy.get('input[name=username]').type('test_user')
      cy.get('input[name=first_name]').type('test_firstname')
      cy.get('input[name=last_name]').type('test_lastname')
      cy.get('input[name=organization]').type('test_organization')
      cy.get('input[name=email]').type('test_user@email.com')
      cy.get('select[name=workspaces]').select('1')
      cy.get('select[name=partner]').select(partner)
      cy.get('input[name=_save]').click()
      cy.get('li[class=success]').contains('successfully')
    })

    it('lets newly created user to login, select response plan, see dashboard', function() {
      //ideally all cy.visit here should be replaced with click()

      //this needs to be moved to a separate describe block and actually login as new user
      cy.visit('/app/BE/cluster-reporting/select-plan', {timeout: 8000})
      cy.wait(6000)
      cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-select-plan', 'h2'])
        .then((res) => {expect(Cypress.$(res).text()).to.contain('Select Response Plan')})
      
      cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-select-plan', 'paper-radio-button'])
        .then((res) => {Cypress.$(res).attr('checked', true)})
     

      // cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-select-plan', 'paper-button[id=confirm]'])
      //   .then((res) => {Cypress.$(res).click()})
      
      cy.visit('/app/BE/cluster-reporting/plan/3/')
      cy.wait(5000)
      cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-router', 'page-cluster-reporting-dashboard', 'page-header', 'h1'])
        .then((res) => {
          expect(Cypress.$(res).text()).to.contain('Partner Dashboard')
        })
      cy.visit('/app/BE/cluster-reporting/plan/3/response-parameters/')
      cy.url().should('contain', 'clusters/objectives')
      cy.wait(5000)
      cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-router', 'page-cluster-reporting-response-parameters', 'clusters-response-parameters', 'page-header', 'h1'])
        .then((res) => {
          expect(Cypress.$(res).text()).to.contain('Clusters')
        })
      cy.visit('/app/BE/cluster-reporting/plan/3/response-parameters/partners')
      cy.wait(7000)
      cy.url().should('contain', 'partners/projects')
      cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-router', 'page-cluster-reporting-response-parameters', 'partners-response-parameters', 'page-header', 'h1'])
        .then((res) => {
          expect(Cypress.$(res).text()).to.contain('Partners')
        })
      cy.visit('/app/BE/cluster-reporting/plan/3/planned-action/')
      cy.wait(5000)
      cy.url().should('contain', 'planned-action/projects')
      cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-router', 'page-cluster-reporting-planned-action', 'page-header', 'h1'])
        .then((res) => {
          expect(Cypress.$(res).text()).to.contain('My Planned Action')
        })
      cy.visit('/app/BE/cluster-reporting/plan/3/results')
      cy.wait(5000)
      cy.url().should('contain', 'results/draft')
      cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-router', 'page-cluster-reporting-results', 'page-header', 'h1'])
        .then((res) => {
          expect(Cypress.$(res).text()).to.contain('Results')
        })
      cy.visit('/app/BE/cluster-reporting/plan/3/analysis')
      cy.wait(5000)
      cy.url().should('contain', 'analysis')
      cy.get('app-shell').shadowDomElement(['page-app', 'page-cluster-reporting', 'page-cluster-reporting-router', 'page-cluster-reporting-analysis', 'page-header', 'h1'])
        .then((res) => {
          expect(Cypress.$(res).text()).to.contain('Analysis')
        })
      })
  })












})