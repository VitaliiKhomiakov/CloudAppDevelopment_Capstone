const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
  try {
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({ authenticator });
    cloudant.setServiceUrl(params.COUCH_URL);

    const dbList = await getDbs(cloudant);
    return dbList;
  } catch (error) {
    console.log(error);
    return { error: error.message };
  }
}

async function getDbs(cloudant) {
  try {
    const result = await cloudant.getAllDbs();
    const dbList = { dbs: result.result };
    return dbList;
  } catch (error) {
    console.log(error);
    throw error;
  }
}

async function getMatchingRecords(cloudant, dbname, selector) {
  try {
    const result = await cloudant.postFind({ db: dbname, selector: selector });
    const matchingRecords = { result: result.result.docs };
    return matchingRecords;
  } catch (error) {
    console.log(error);
    throw error;
  }
}

async function getAllRecords(cloudant, dbname) {
  try {
    const result = await cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 });
    const allRecords = { result: result.result.rows };
    return allRecords;
  } catch (error) {
    console.log(error);
    throw error;
  }
}
