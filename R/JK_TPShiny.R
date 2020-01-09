library(shiny)
library(tidyverse)
library(leaflet)

# Préparation des données
data=read_delim("data/data_commerces_shiny.csv",
                ";", escape_double = FALSE, trim_ws = TRUE,
                locale=locale(encoding="ISO-8859-1")
) %>% mutate(DDEBACT=lubridate::ymd(DDEBACT), DCREN=lubridate::ymd(DCREN))

ui <- fluidPage(

    titlePanel("Exercice Shiny"),
    navlistPanel(
        tabPanel("Table",
                 radioButtons("ndep", label = "Numéro de département",
                              choices = unique(data$DEPET)),
                 checkboxInput("entete", label = "Montrer l'en-tête seulement"),
                 DT::dataTableOutput("tdep")
        ),
        tabPanel("Résultats",
                 splitLayout(
                     cellWidths = c("25%", "75%"),
                     radioButtons("type", label = "Type", 
                                  choices = unique(data$type)),
                     tabsetPanel(
                         tabPanel("Graphique 1", plotOutput("g1")),
                         tabPanel("Graphique 2", plotOutput("g2")),
                         tabPanel("Carte", tmapOutput("carte"))
                     )
                 )
        )
    )
    
)

server <- function(input, output) {

    # Rendu du tableau
    output$tdep = DT::renderDataTable({
        out = data %>% filter(DEPET == input$ndep)
        if(input$entete) out = head(out, 3)
        out
    })
    
    # Rendu du graphique 1
    output$g1 = renderPlot({
        ggplot(data = data %>% filter(type == input$type), aes(DDEBACT)) + 
            geom_histogram(binwidth = 1000, fill = "orange")
    })
    
    # Rendu du graphique 2
    output$g2 = renderPlot({
        ggplot(data = data %>% filter(type == input$type), aes(EFETCENT)) + 
            geom_bar(fill = "pink")
    })
    
    # Rendu de la carte
    output$carte = renderLeaflet({
        data_f = data %>% filter(type == input$type)
        leaflet() %>%
            addProviderTiles(
                providers$OpenStreetMap.Mapnik,
                options = providerTileOptions(noWrap = TRUE)
            ) %>% addCircles(data = data_f, color = "gray", label = data_f$SIREN)
    })

}

# Run the application 
shinyApp(ui = ui, server = server)
