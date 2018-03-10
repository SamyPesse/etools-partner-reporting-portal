# OCHA Integration

High level we'll be integrating with [OCHA](https://www.unocha.org/) systems to import:

**\(TBD  Maciej waiting on RPM to finish disaggregations and locations info for indicator. Hoping for confirmation ~March 15th \)**

* Response plan and its details \(RPM\):
  * Response plan
  * Associated clusters
  * Cluster objectives and indicators 
  * Cluster activities and indicators
  * Partners associated with the response plan **\(TBD Maciej will look into this\)**
* Partner Projects and Partner activities \(OPS?\):
  * Projects and their indicators
  * Activities and their indicators
* FTS **\(TBD Maciej will look into this\)**

IMO and partner users will still be able to add custom response plan, or new cluster objectives/activities, partner projects/activities etc. as per usual.

Platform allows to search all active Response Plans stored in RPM API in selected Workspace. Basic information is dynamically pulled out from API:

* Plan Type
* Clusters
* Start Date
* End Date

Saving Response Plan triggers background synchronization of:

* Cluster activities
* Cluster objectives
* Indicators



