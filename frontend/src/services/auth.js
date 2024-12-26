import { doRequest } from "./client";

export const processAuth = async ({ login, password }) => {
  const response = await doRequest({
    type: "POST",
    uri: "/login",
    body: {
      login: login,
      password: password,
    },
  });
  console.log("Login: response:", response);

  return response;
};

