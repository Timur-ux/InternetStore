import client, { doRequest, RequestType } from "./client"

export const getBalance = async () => {
  const result = await client.get("/user/balance");
  return result;
}

export const balanceTopUp = async (amount) => {
  const result = await doRequest({type: RequestType.post, uri: "/user/balance/top-up", params: {
    amount: amount
  }});

  return result;
}
