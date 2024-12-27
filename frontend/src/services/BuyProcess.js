import { setBalance } from "../app/reducers/authData";
import { doRequest, RequestType } from "./client";

export const BuyProcess = async (items, token = "", dispatch) => {
  const uris = items.map((item) => item.uri);

  const response = await doRequest(
    {
      type: RequestType.post,
      uri: "/purchase",
      body: {
        uris: uris,
      },
    },
    token,
  );

  doRequest(
    {
      type: RequestType.get,
      uri: "/user/balance",
    },
    token,
  )
    .then((response) => {
      dispatch(setBalance(response.data.balance));
    })
    .catch((reason) => {
      console.log("BuyProcess: balance update: error: ", reason);
    });

  console.log("BuyProcess: response: ", response);
  return response;
};
