# Common settings for all chapters (sourced in a hidden chunk at the top of each chapter)

knitr::opts_chunk$set(
  comment = "##",
  fig.align = "center",
  fig.width = 7,
  fig.height = 4,
  fig.retina = 2,
  message = FALSE,
  warning = FALSE
)

suppressPackageStartupMessages(library(ggplot2))

timera_palette <- c("#0072B2", "#D55E00", "#009E73", "#CC79A7",
                    "#E69F00", "#56B4E9", "#7F7F7F")

theme_set(
  theme_minimal(base_size = 12) +
    theme(
      panel.grid.minor = element_blank(),
      legend.position = "bottom",
      plot.title.position = "plot",
      strip.text = element_text(face = "bold")
    )
)
options(
  ggplot2.discrete.colour = timera_palette,
  ggplot2.discrete.fill = timera_palette
)
