const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.COUCH_URL);

  let dbList = [];
  try {
    dbList = await getDbs(cloudant);
  } catch (err) {
    console.log(err);
  }
  return { dbs: dbList };
}

async function getDbs(cloudant) {
  const body = await cloudant.getAllDbs();
  return body;
}
