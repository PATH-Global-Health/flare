import * as actionTypes from "../actions/actionTypes";

const initialState = {
  data: [],
  count: 0,
  loadingLanguages: false,
  saveSuccess: false,
  error: null,
  language: null,
  loadingLanguage: false,
  lookup: {},
  loadingLookup: false,
};

const fetchLanguagesStart = (state) => {
  return {
    ...state,
    error: null,
    loadingLanguages: true,
  };
};

const fetchLanguagesSuccess = (state, action) => {
  return {
    ...state,
    data: action.data,
    loadingLanguages: false,
    error: null,
    count: action.count,
  };
};

const fetchLanguagesFail = (state, action) => {
  return {
    ...state,
    loadingLanguages: false,
    error: action.error,
  };
};

const saveLanguageSuccess = (state) => {
  return {
    ...state,
    saveSuccess: true,
  };
};

const resetSaveLanguageSuccess = (state, action) => {
  return {
    ...state,
    saveSuccess: false,
  };
};

const fetchLanguageStart = (state) => {
  return {
    ...state,
    error: null,
    loadingLanguage: true,
  };
};

const fetchLanguageSuccess = (state, action) => {
  return {
    ...state,
    language: action.language,
    loadingLanguage: false,
  };
};

const removeLanguageFromList = (state, action) => {
  return {
    ...state,
    data: state.data.filter((el) => el.id !== action.langId),
  };
};

const updateLanguageFail = (state, action) => {
  return {
    ...state,
    error: action.error,
  };
};

const fetchLanguagesLookupStart = (state) => {
  return {
    ...state,
    error: null,
    loadingLookup: true,
  };
};

const fetchLanguagesLookupSuccess = (state, action) => {
  return {
    ...state,
    lookup: action.lookup,
    loadingLookup: false,
    error: null,
  };
};

const fetchLanguagesLookupFail = (state, action) => {
  return {
    ...state,
    loadingLookup: false,
    error: action.error,
  };
};

const reducer = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.FETCH_LANGUAGES_START:
      return fetchLanguagesStart(state);
    case actionTypes.FETCH_LANGUAGES_SUCCESS:
      return fetchLanguagesSuccess(state, action);
    case actionTypes.FETCH_LANGUAGES_FAIL:
      return fetchLanguagesFail(state, action);
    case actionTypes.SAVE_LANGUAGE_SUCCESS:
      return saveLanguageSuccess(state);
    case actionTypes.RESET_SAVE_LANGUAGE_SUCCESS:
      return resetSaveLanguageSuccess(state);
    case actionTypes.FETCH_LANGUAGE_START:
      return fetchLanguageStart(state);
    case actionTypes.FETCH_LANGUAGE_SUCCESS:
      return fetchLanguageSuccess(state, action);
    case actionTypes.REMOVE_LANGUAGE:
      return removeLanguageFromList(state, action);
    case actionTypes.UPDATE_LANGUAGE_FAIL:
      return updateLanguageFail(state, action);
    case actionTypes.FETCH_LANGUAGES_LOOKUP_START:
      return fetchLanguagesLookupStart(state);
    case actionTypes.FETCH_LANGUAGES_LOOKUP_SUCCESS:
      return fetchLanguagesLookupSuccess(state, action);
    case actionTypes.FETCH_LANGUAGES_LOOKUP_FAIL:
      return fetchLanguagesLookupFail(state, action);
    default:
      return state;
  }
};

export default reducer;
