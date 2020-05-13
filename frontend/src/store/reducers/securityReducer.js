import * as actionTypes from "../actions/actionTypes";

const initialState = {
  isAuthenticated: false,
  user: {},
  error: null,
  loading: false,
  timer: null,
};

const authStart = (state, action) => {
  return {
    ...state,
    error: null,
    loading: true,
  };
};

const authSuccess = (state, action) => {
  return {
    ...state,
    isAuthenticated: true,
    user: {
      id: action.id,
      username: action.username,
      email: action.email,
    },
    error: null,
    loading: false,
  };
};

const authFail = (state, action) => {
  return {
    ...state,
    isAuthenticated: false,
    error: action.error,
    loading: false,
  };
};

const authLogout = (state, action) => {
  return {
    ...state,
    isAuthenticated: false,
    user: {},
  };
};

const authSetTimeout = (state, action) => {
  return {
    ...state,
    timer: action.timer,
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.AUTH_START:
      return authStart(state, action);
    case actionTypes.AUTH_SUCCESS:
      return authSuccess(state, action);
    case actionTypes.AUTH_FAIL:
      return authFail(state, action);
    case actionTypes.AUTH_LOGOUT:
      return authLogout(state, action);
    case actionTypes.AUTH_SET_TIMER:
      return authSetTimeout(state, action);
    default:
      return state;
  }
};

export default reducer;
