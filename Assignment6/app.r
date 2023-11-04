# load packages
library("ggplot2")
library("RColorBrewer")
library("ggExtra")
library("shiny")
library("rsconnect")

# define UI
ui <- fluidPage(
    titlePanel("Plant CO2 Uptake vs Surrounding CO2 
    Concentration (Scatter Plot)"),

    sidebarPanel(

        checkboxGroupInput(
            inputId="plant", 
            label="Choose which plants to visualize",
            choices = unique(CO2$Plant),
            selected=levels(CO2$Plant)
        ),

        selectInput(
            inputId="comparison",
            label="What would you like to compare?",
            choices = c(
                "Treatment",
                "Type"
            ),
            selected="Treatment"
        )
    ),

    mainPanel(
        plotOutput("scatter_plot"),
        plotOutput("line_plot")
    )
)

# define server function
server <- function(input, output) {

    output$scatter_plot <- renderPlot({

        data <- subset(
            CO2,
            CO2[, "Plant"] %in% input$plant
        )

        ggplot(data) +
            geom_point(
                aes(
                    x = data$conc,
                    y = data$uptake,
                    color = data$Plant
                ),
                size = 4
            ) +

            xlab("Environmental CO2 Concentration") +
            ylab("Plant CO2 Uptake") +

            theme_bw() +

            theme(
                axis.text.x = element_text(
                    face = "bold",
                    color = "black",
                    size = 10,
                    angle = 0
                ),
                axis.text.y = element_text(
                    face = "bold",
                    color = "black",
                    size = 10,
                    angle = 0
                )
            )
    })

    output$line_plot <- renderPlot({

        data <- subset(
            CO2,
            CO2[, "Plant"] %in% input$plant
        )

        ggplot(data) +
            geom_smooth(
                aes(
                    x = data$conc,
                    y = data$uptake,
                    color = data$Plant,
                    linetype = data[, input$comparison]
                ),
                method = "lm",
                formula = y ~ log(x),
                se = FALSE
            ) +

            xlab("Environmental CO2 Concentration") +
            ylab("Plant CO2 Uptake") +

            theme_bw() +

            theme(
                axis.text.x = element_text(
                    face = "bold",
                    color = "black",
                    size = 10,
                    angle = 0
                ),
                axis.text.y = element_text(
                    face = "bold",
                    color = "black",
                    size = 10,
                    angle = 0
                )
            )
    })
}

shinyApp(
    ui=ui, 
    server=server
)