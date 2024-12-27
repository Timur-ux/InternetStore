import { doRequest, RequestType } from "./client";

export const doForecast = async (items, token = "") => {
  const item_uris = items.map((item) => {
    return item.uri;
  });

  const response = await doRequest(
    {
      type: RequestType.post,
      uri: "/admin/forecast",
      body: {
        uris: item_uris,
      },
    },
    token,
  );
  console.log("doForecast: response:", response);

  return response;
};
