package main

import (
    "net/http"
    "fmt"
    "time"
    "errors"
    "log"
    "strconv"
    "encoding/json"

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
    w.Header().Set("Content-Type", "application/json; charset=utf-8")
}

/*
 * Models
 */

type Article struct {
    Id      int     `json:"id"`
    Title   string  `json:"title"`
    Created string  `json:"created"`
    Status  string  `json:"status"`
}

type Articles []Article

/*
 * Repository
 */

var articles Articles
var lastArticleId = 0

func GetArticles() (Articles) {
    // filter deleted articles
    newArticles := Articles{}
    for _, a := range articles {
        if a.Status != "deleted" {
            newArticles = append(newArticles, a)
        }
    }
    return newArticles
}

func GetArticleById(id int) (Article, error) {
	for _, a := range articles {
		if a.Id == id && a.Status != "deleted" {
            return a, nil
		}
	}
    return Article{}, errors.New("Article not found")
}

func AddArticle(article Article) (Article, error) {
    if len(article.Title) == 0 {
        return Article{}, errors.New("Title is required")
    }
    article.Id = lastArticleId + 1
    article.Created = time.Now().UTC().Format(time.RFC3339)
    article.Status = "created"
    articles = append(articles, article)
    lastArticleId += 1
    return article, nil
}

func UpdateArticle(article Article) (Article, error) {
    if len(article.Title) == 0 {
        return Article{}, errors.New("Title is required")
    }
	for i, a := range articles {
		if a.Id == article.Id {
            articles[i].Title = article.Title
            return articles[i], nil
		}
	}
    return Article{}, errors.New("Article not found")
}

func DeleteArticle(id int) (Article, error) {
	for i, a := range articles {
		if a.Id == id {
            articles[i].Status = "deleted"
            return articles[i], nil
		}
	}
    return Article{}, errors.New("Article not found")
}

/*
 * Main
 */

func ListArticlesHandler(w http.ResponseWriter, r *http.Request) {
    SetHeaders(w)

    articles := GetArticles()
    json.NewEncoder(w).Encode(articles)
}

func GetArticleHandler(w http.ResponseWriter, r *http.Request) {
    SetHeaders(w)

    vars := mux.Vars(r)
    id, err := strconv.Atoi(vars["id"])
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    article, err := GetArticleById(id)
    if err != nil {
        http.Error(w, err.Error(), http.StatusNotFound)
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
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    article, err = AddArticle(article)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
}

func UpdateArticleHandler(w http.ResponseWriter, r *http.Request) {
    SetHeaders(w)

    vars := mux.Vars(r)
    id, err := strconv.Atoi(vars["id"])
    if err != nil {
        http.Error(w, err.Error(), 404)
        return
    }
    article := Article{Id: id}
    err = json.NewDecoder(r.Body).Decode(&article)
    if err != nil {
        log.Println("Unable to deserialize body", err)
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    article, err = UpdateArticle(article)
    if err != nil {
        http.Error(w, err.Error(), http.StatusNotFound)
        return
    }
}

func DeleteArticleHandler(w http.ResponseWriter, r *http.Request) {
    SetHeaders(w)

    vars := mux.Vars(r)
    id, err := strconv.Atoi(vars["id"])
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    _, err = DeleteArticle(id)
    if err != nil {
        http.Error(w, err.Error(), http.StatusNotFound)
        return
    }
}

func main() {
    // Setup Fixtures
    AddArticle(Article{Title: "First!"})
    AddArticle(Article{Title: "Second Article"})
    AddArticle(Article{Title: "Third Article"})
    DeleteArticle(3)

    fmt.Println("Server started")

    r := mux.NewRouter()
    r.Use(loggingMiddleware)
    r.HandleFunc("/articles", ListArticlesHandler).Methods("GET")
    r.HandleFunc("/articles/{id:[0-9]+", GetArticleHandler).Methods("GET")
    r.HandleFunc("/articles", CreateArticleHandler).Methods("POST")
    r.HandleFunc("/articles/{id:[0-9]+}", UpdateArticleHandler).Methods("POST")
    r.HandleFunc("/articles/{id:[0-9]+}", DeleteArticleHandler).Methods("DELETE")

    log.Fatal(http.ListenAndServe("localhost:8000", r))
}
