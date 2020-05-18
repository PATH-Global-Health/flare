import * as actionTypes from "../actions/actionTypes";

const initialState = {
  data: [],
  error: null,
  loading: false,
};

const fetchDashboardDataStart = (state) => {
  return {
    ...state,
    error: null,
    loading: true,
  };
};

const fetchDashboardDataSuccess = (state, action) => {
  return {
    ...state,
    data: action.data,
    loading: false,
    error: null,
  };
};

const fetchDashboardDataFail = (state, action) => {
  return {
    ...state,
    loading: false,
    error: action.error,
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_DASHBOARD_DATA_START:
      return fetchDashboardDataStart(state);
    case actionTypes.FETCH_DASHBOARD_DATA_SUCCESS:
      return fetchDashboardDataSuccess(state, action);
    case actionTypes.FETCH_DASHBOARD_DATA_FAIL:
      return fetchDashboardDataFail(state, action);
    default:
      return state;
  }
};

export default reducer;
