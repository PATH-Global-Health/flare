import * as actionTypes from "./actionTypes";
import axios from "../../helpers/axiosFlare";
import mapResponseErrors from "../../helpers/mapResponseErrors";
import { logout } from "./securityActions";

export const fetchLanguagesSuccess = (languages, count) => {
  return {
    type: actionTypes.FETCH_LANGUAGES_SUCCESS,
    data: languages,
    count: count,
  };
};

export const fetchLanguagesFail = (error) => {
  return {
    type: actionTypes.FETCH_LANGUAGES_FAIL,
    error: error,
  };
};

export const fetchLanguagesStart = () => {
  return {
    type: actionTypes.FETCH_LANGUAGES_START,
  };
};

export const fetchLanguages = (limit, offset, searchTerm) => {
  return (dispatch) => {
    dispatch(fetchLanguagesStart());

    axios
      .get(`/languages/?limit=${limit}&offset=${offset}&search=${searchTerm}`)
      .then((res) => {
        const languages = [];
        const count = res.data.count;

        res.data.results.forEach((lang, index) => languages.push({ ...lang }));

        dispatch(fetchLanguagesSuccess(languages, count));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchLanguagesFail(err.message));
        } else {
          if (err.response.status === 401 || err.response.status === 403) {
            dispatch(logout());
          } else {
            dispatch(fetchLanguagesFail(err.response.data.message));
          }
        }
      });
  };
};

export const saveDelLanguageSuccess = () => {
  return {
    type: actionTypes.SAVE_LANGUAGE_SUCCESS,
  };
};

export const resetSaveLanguageSuccess = () => {
  return {
    type: actionTypes.RESET_SAVE_LANGUAGE_SUCCESS,
  };
};

export const updateLanguageFail = (error) => {
  return {
    type: actionTypes.UPDATE_LANGUAGE_FAIL,
    error: error,
  };
};

export const addLanguage = (lang, history, errorCallback) => {
  return (dispatch) => {
    axios
      .post("/languages/", lang)
      .then((res) => {
        dispatch(saveDelLanguageSuccess());
        history.push("/language");
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(updateLanguageFail(err.message));
          errorCallback(err.message);
        } else {
          const errors = mapResponseErrors(err.response.data);
          errorCallback(errors);
        }
      });
  };
};

export const fetchLanguageSuccess = (language) => {
  return {
    type: actionTypes.FETCH_LANGUAGE_SUCCESS,
    language: language,
  };
};

export const fetchLanguageStart = () => {
  return {
    type: actionTypes.FETCH_LANGUAGE_START,
  };
};

export const fetchLanguage = (langId, history) => {
  return (dispatch) => {
    dispatch(fetchLanguageStart());

    axios
      .get(`/languages/${langId}`)
      .then((res) => {
        const language = {
          code: res.data.code,
          name: res.data.name,
        };

        dispatch(fetchLanguageSuccess(language));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchLanguagesFail(err.message));
        } else {
          dispatch(fetchLanguagesFail(err.response.data.message));
        }
        history.push("/language/");
      });
  };
};

export const editLanguage = (lang, langId, history, errorCallback) => {
  return (dispatch) => {
    axios
      .put(`/languages/${langId}/`, lang)
      .then((res) => {
        dispatch(saveDelLanguageSuccess());
        history.push("/language");
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(updateLanguageFail(err.message));
          errorCallback(err.message);
        } else {
          const errors = mapResponseErrors(err.response.data);
          errorCallback(errors);
        }
      });
  };
};

export const removeLanguageFromList = (langId) => {
  return {
    type: actionTypes.REMOVE_LANGUAGE,
    langId: langId,
  };
};

export const deleteLanguage = (langId, history) => {
  return (dispatch) => {
    axios
      .delete(`/languages/${langId}/`)
      .then((res) => {
        dispatch(saveDelLanguageSuccess());
        dispatch(removeLanguageFromList(langId));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchLanguagesFail(err.message));
        } else {
          dispatch(fetchLanguagesFail(err.response.data.message));
        }
      });
  };
};

export const fetchLanguagesLookupSuccess = (lookup) => {
  return {
    type: actionTypes.FETCH_LANGUAGES_LOOKUP_SUCCESS,
    lookup: lookup,
  };
};

export const fetchLanguagesLookupFail = (error) => {
  return {
    type: actionTypes.FETCH_LANGUAGES_LOOKUP_FAIL,
    error: error,
  };
};

export const fetchLanguagesLookupStart = () => {
  return {
    type: actionTypes.FETCH_LANGUAGES_LOOKUP_START,
  };
};

export const fetchLanguagesLookup = () => {
  return (dispatch) => {
    dispatch(fetchLanguagesLookupStart());

    axios
      .get("/languages/?limit=1000")
      .then((res) => {
        const lookup = [];

        res.data.results.forEach((lang, index) =>
          lookup.push({ value: lang.id, label: lang.name })
        );

        dispatch(fetchLanguagesLookupSuccess(lookup));
      })
      .catch((err) => {
        if (err.response === undefined) {
          dispatch(fetchLanguagesLookupFail(err.message));
        } else {
          if (err.response.status === 401 || err.response.status === 403) {
            dispatch(logout());
          } else {
            dispatch(fetchLanguagesLookupFail(err.response.data.message));
          }
        }
      });
  };
};
