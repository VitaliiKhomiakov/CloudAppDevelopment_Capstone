const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main({ IAM_API_KEY, COUCH_URL }) {
  const authenticator = new IamAuthenticator({ apikey: IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({ authenticator });
  cloudant.setServiceUrl(COUCH_URL);

  try {
    const result = await cloudant.getAllDbs();
    const dbList = result.result;
    return { dbs: dbList };
  } catch (err) {
    return { error: err.message };
  }
}
