import * as actionTypes from "../actions/actionTypes";

const initialState = {
  data: [],
  count: 0,
  loadingResults: false,
  error: null,
};

const fetchResultsStart = (state) => {
  return {
    ...state,
    error: null,
    loadingResults: true,
  };
};

const fetchResultsSuccess = (state, action) => {
  return {
    ...state,
    data: action.data,
    loadingResults: false,
    error: null,
    count: action.count,
    deleteSuccess: false,
  };
};

const fetchResultsFail = (state, action) => {
  return {
    ...state,
    loadingResults: false,
    error: action.error,
  };
};

const deleteResultSuccess = (state, action) => {
  return {
    ...state,
    deleteSuccess: true,
  };
};

const removeResultFromList = (state, action) => {
  return {
    ...state,
    data: state.data.filter((el) => el.id !== action.resultId),
  };
};

const resetDeleteResultSuccess = (state, action) => {
  return {
    ...state,
    deleteSuccess: false,
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_RESULTS_START:
      return fetchResultsStart(state);
    case actionTypes.FETCH_RESULTS_SUCCESS:
      return fetchResultsSuccess(state, action);
    case actionTypes.FETCH_RESULTS_FAIL:
      return fetchResultsFail(state, action);
    case actionTypes.DELETE_RESULT_SUCCESS:
      return deleteResultSuccess(state, action);
    case actionTypes.REMOVE_RESULT:
      return removeResultFromList(state, action);
    case actionTypes.RESET_DELETE_RESULT_SUCCESS:
      return resetDeleteResultSuccess(state, action);
    default:
      return state;
  }
};

export default reducer;
