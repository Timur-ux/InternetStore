import { setToken, setUserType, UserType } from "../app/reducers/authData";
import { doRequest } from "./client";
import { RequestType } from "./client";
import { setBalance } from "../app/reducers/authData";
import { addMenuItems } from "../app/reducers/menuItems";

export const processAuth = async (dispatch, { login, password }) => {
  const response = await doRequest({
    type: "POST",
    uri: "/login",
    body: {
      login: login,
      password: password,
    },
  });
  console.log("Login: response:", response);
  if (response.data.user_type == "Администратор") {
    dispatch(setUserType(UserType.admin));
    dispatch(
      addMenuItems([
        {
          id: 2,
          name: "Сделать прогноз продаж",
          path: "/forecast",
        },
      ]),
    );
  } else {
    dispatch(setUserType(UserType.user));
  }

  dispatch(setToken(response.data.token));
  await doRequest(
    {
      type: RequestType.post,
      uri: "/user/balance/top-up",
      body: { amount: 1000 },
    },
    response.data.token,
  ).catch((reason) => {
    console.log("Log in process: error: couldn't top up balance: ", reason);
  });

  await doRequest(
    { type: RequestType.get, uri: "/user/balance" },
    response.data.token,
  )
    .then((response) => {
      dispatch(setBalance(response.data.balance));
    })
    .catch((reason) => {
      dispatch(setBalance(-1));
      console.log("Log in process: error: ", reason);
    });

  return response;
};
