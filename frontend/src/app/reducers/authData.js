import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  data: {
    status: "notLoggedIn",
    login: "",
    password: "",
  },
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setLogin(state, action) {
      state.data.login = action.payload;
    },
    setPassword(state, action) {
      console.log("Set password: ", action.payload);
      state.data.password = action.payload;
    },
    onLogIn(state, action) {
      state.data.status = "loggedIn";
    },
    onLogOut(state, action) {
      state.data.status = initialState.data.status;
    },
  },
});

export const { setLogin, setPassword, onLogOut, onLogIn} = authSlice.actions;
export default authSlice.reducer;

export const selectAuthData = (state) => state.auth.data;
