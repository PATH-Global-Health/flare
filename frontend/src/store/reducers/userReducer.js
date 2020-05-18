import * as actionTypes from "../actions/actionTypes";

const initialState = {
  data: [],
  error: null,
  loading: false,
};

const fetchUserStart = (state) => {
  return {
    ...state,
    error: null,
    loading: true,
  };
};

const fetchUserSuccess = (state, action) => {
  return {
    ...state,
    data: action.data,
    loading: false,
    error: null,
  };
};

const fetchUserFail = (state, action) => {
  return {
    ...state,
    loading: false,
    error: action.error,
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_USER_START:
      return fetchUserStart(state);
    case actionTypes.FETCH_USER_SUCCESS:
      return fetchUserSuccess(state, action);
    case actionTypes.FETCH_USER_FAIL:
      return fetchUserFail(state, action);
    default:
      return state;
  }
};

export default reducer;
