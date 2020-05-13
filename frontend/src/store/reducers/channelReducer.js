import * as actionTypes from "../actions/actionTypes";

const initialState = {
  loadingLookup: false,
  error: null,
  lookup: {},
};

const fetchChannelsLookupStart = (state) => {
  return {
    ...state,
    error: null,
    loadingLookup: true,
  };
};

const fetchChannelsLookupSuccess = (state, action) => {
  return {
    ...state,
    lookup: action.lookup,
    loadingLookup: false,
    error: null,
  };
};

const fetchChannelsLookupFail = (state, action) => {
  return {
    ...state,
    loadingLookup: false,
    error: action.error,
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_CHANNELS_LOOKUP_START:
      return fetchChannelsLookupStart(state);
    case actionTypes.FETCH_CHANNELS_LOOKUP_SUCCESS:
      return fetchChannelsLookupSuccess(state, action);
    case actionTypes.FETCH_CHANNELS_LOOKUP_FAIL:
      return fetchChannelsLookupFail(state, action);
    default:
      return state;
  }
};

export default reducer;
