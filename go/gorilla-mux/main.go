package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/gorilla/mux"
)

/*
 * Utils
 */

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("%s %s", r.Method, r.RequestURI)
		next.ServeHTTP(w, r)
	})
}

func SetHeaders(w http.ResponseWriter) {
	w.Header().Set("Content-Type", "application/json")
}

/*
 * Models
 */

type Article struct {
	Id      int    `json:"id"`
	Title   string `json:"title"`
	Created string `json:"created"`
	Status  string `json:"status"`
}

type Articles []Article

type ArticleRepository struct {
	Articles Articles
	lastId int
}

func (repo *ArticleRepository) GetById(id int) (Article, error) {
	for _, a := range repo.Articles {
		if a.Id == id && a.Status != "deleted" {
			return a, nil
		}
	}
	return Article{}, errors.New("Article not found")
}

func (repo *ArticleRepository) List() (Articles) {
	createdArticles := Articles{}
	for _, a := range repo.Articles {
		if a.Status != "deleted" {
			createdArticles = append(createdArticles, a)
		}
	}
	return createdArticles
}

func (repo *ArticleRepository) Add(a Article) (Article, error) {
	if len(a.Title) == 0 {
		return Article{}, errors.New("Title is required")
	}
	a.Id = repo.lastId + 1
	a.Created = time.Now().UTC().Format(time.RFC3339)
	a.Status = "created"
	repo.Articles = append(repo.Articles, a)
	repo.lastId += 1
	return a, nil
}

func (repo *ArticleRepository) Update(article Article) (Article, error) {
	if len(article.Title) == 0 {
		return Article{}, errors.New("Title is required")
	}
	for i, a := range repo.Articles {
		if a.Id == article.Id {
			repo.Articles[i].Title = article.Title
			return repo.Articles[i], nil
		}
	}
	return Article{}, fmt.Errorf("Article \"%v\"not found", article.Id)
}

func (repo *ArticleRepository) Delete(id int) (Article, error) {
	for i, a := range repo.Articles {
		if a.Id == id && a.Status != "deleted" {
			repo.Articles[i].Status = "deleted"
			return repo.Articles[i], nil
		}
	}
	return Article{}, errors.New("Article not found")
}

var repo ArticleRepository

type JsonErrorResponse struct {
	Code    int      `json:"code"`
	Message string `json:"message"`
}

/*
 * Main
 */

func ListArticlesHandler(w http.ResponseWriter, r *http.Request) {
	SetHeaders(w)
	articles := repo.List()
	json.NewEncoder(w).Encode(articles)
}

func GetArticleHandler(w http.ResponseWriter, r *http.Request) {
	SetHeaders(w)
	id, _ := strconv.Atoi(mux.Vars(r)["id"])

	article, err := repo.GetById(id)
	if err != nil {
		w.WriteHeader(http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(article)
}

func CreateArticleHandler(w http.ResponseWriter, r *http.Request) {
	SetHeaders(w)

	var article Article

	err := json.NewDecoder(r.Body).Decode(&article)
	if err != nil {
		log.Println("Unable to deserialize body", err)
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	article, err = repo.Add(article)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		return
	}

	url := fmt.Sprintf("/articles/%d", article.Id)
	w.Header().Set("Location", url)
	w.WriteHeader(http.StatusCreated)

	json.NewEncoder(w).Encode(article)
}

func UpdateArticleHandler(w http.ResponseWriter, r *http.Request) {
	SetHeaders(w)
	id, _ := strconv.Atoi(mux.Vars(r)["id"])

	article := Article{Id: id}
	err := json.NewDecoder(r.Body).Decode(&article)
	if err != nil {
		log.Println("Unable to deserialize body", err)
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	article, err = repo.Update(article)
	if err != nil {
		w.WriteHeader(http.StatusNotFound)
		myError := JsonErrorResponse{1, "Could not add article"}
		wrapped := map[string]interface{}{"error": myError}
		json.NewEncoder(w).Encode(wrapped)
		return
	}

	json.NewEncoder(w).Encode(article)
}

func DeleteArticleHandler(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(mux.Vars(r)["id"])

	_, err := repo.Delete(id)
	if err != nil {
		w.WriteHeader(http.StatusNotFound)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

func main() {
	// Fixtures
	// Testing only
	repo.Add(Article{Title: "First!"})
	repo.Add(Article{Title: "Second Article"})
	repo.Add(Article{Title: "Third Article"})
	repo.Delete(3)

	fmt.Println("Server started")

	r := mux.NewRouter()
	r.Use(loggingMiddleware)
	r.HandleFunc("/articles", ListArticlesHandler).Methods("GET")
	r.HandleFunc("/articles/{id:[0-9]+}", GetArticleHandler).Methods("GET")
	r.HandleFunc("/articles", CreateArticleHandler).Methods("POST")
	r.HandleFunc("/articles/{id:[0-9]+}", UpdateArticleHandler).Methods("PUT")
	r.HandleFunc("/articles/{id:[0-9]+}", DeleteArticleHandler).Methods("DELETE")

	log.Fatal(http.ListenAndServe("localhost:8000", r))
}
