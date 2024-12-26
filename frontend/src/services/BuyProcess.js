import client, { doRequest, RequestType } from "./client";

export const BuyProcess = async (items) => {
  const uris = items.map((item) => item.uri);

  const response = await doRequest(
    {
      type: RequestType.post, uri: "/buy", body: {
        item_uris: uris
      }
    }
  );

  console.log("BuyProcess: response: ", response);
  return response;
}
