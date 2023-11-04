library("ggplot2")
library("httpgd")
library("RColorBrewer")
library("ggExtra")

hgd()
hgd_browse()

scatter_plot <- ggplot(CO2) +
    geom_point(
        aes(
            x = conc,
            y = uptake,
            color = Plant
        ),
        size = 4
    ) +

    ggtitle("Plant CO2 Uptake vs Surrounding CO2 Concentration (Scatter Plot)") +

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

print(scatter_plot)

line_plot <- ggplot(CO2) +
    geom_smooth(
        aes(
            x = conc,
            y = uptake,
            color = Plant,
            linetype = Treatment
        ),
        method = "lm",
        formula = y ~ log(x),
        se = FALSE
    ) +

    ggtitle("Plant CO2 Uptake vs Surrounding CO2 Concentration (Logarithmic Plot)") +

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

print(line_plot)

hgd_close()
