library(BatchCorrMetabolomics)
data(BC)

set.3.lod <- min(set.3[!is.na(set.3)])
minBatchOccurrence.Ave <- 2
minBatchOccurrence.Line <- 4


TOF.ngenotypes <- nlevels(set.3.Y$SCode)-1 ## take away the ref samples
TOF.nNA <- apply(set.3, 2, function(x) sum(is.na(x)))
TOF.nref <- sum(set.3.Y$SCode == "ref")


conditions <- c("", "0", "1", "2", "c")
experiments <- c(t(outer(c("Q", "S"), conditions, paste, sep = "")))
methods <- rep("lm", length(experiments))
methods[grep("c", experiments)] <- "tobit"
imputeValues <- rep(NA, length(experiments))
imputeValues[grep("0", experiments)] <- 0
imputeValues[grep("1", experiments)] <- set.3.lod / 2
imputeValues[grep("2", experiments)] <- set.3.lod
imputeValues[grep("c", experiments)] <- set.3.lod - .01
refSamples <- list("Q" = which(set.3.Y$SCode == "ref"),
                   "S" = which(set.3.Y$SCode != "ref"))
strategies <- rep(c("Q", "S"), each = length(conditions))

## leave out the censored regressions for A
exp.idx <- (1:length(experiments))[-grep("c", experiments)]
suppressMessages(allResultsAve <-
                   lapply(exp.idx,
                          function(ii)
                            apply(set.3, 2, doBC,
                                  ref.idx = refSamples[[ strategies[[ii]] ]],
                                  batch.idx = set.3.Y$Batch,
                                  minBsamp = minBatchOccurrence.Ave,
                                  correctionFormula = formula("X ~ B"),
                                  seq.idx = set.3.Y$SeqNr,
                                  method = methods[ii],
                                  imputeVal = imputeValues[ii])))
names(allResultsAve) <- experiments[exp.idx]

suppressMessages(allResultsLine <-
                   lapply(seq(along = experiments),
                          function(ii)
                            apply(set.3, 2, doBC,
                                  ref.idx = refSamples[[ strategies[[ii]] ]],
                                  batch.idx = set.3.Y$Batch,
                                  minBsamp = minBatchOccurrence.Line,
                                  seq.idx = set.3.Y$SeqNr,
                                  method = methods[ii],
                                  imputeVal = imputeValues[ii])))
names(allResultsLine) <- experiments

library("RUVSeq")

idx <- which(set.3.Y$SCode == "ref")
replicates.ind <- matrix(-1, nrow(set.3) - length(idx) + 1, length(idx))
replicates.ind[1,] <- idx
replicates.ind[-1,1] <- (1:nrow(set.3))[-idx]

allResultsRUV <-
  lapply(0:2,
         function(ImpVal) {
           huhn <- set.3
           huhn[is.na(huhn)] <- ImpVal * set.3.lod / 2
           woppa <- t(RUVs(t(huhn),
                           1:ncol(huhn),
                           k = 3,
                           replicates.ind,
                           round = FALSE, isLog = TRUE)$normalizedCounts)
           woppa[is.na(set.3)] <- NA
           woppa
         })


# figure 2

par(mfrow = c(1,1))
huhnPCA <- evaluateCorrection(set.3, set.3.Y, what = "PCA",
                              plot = TRUE, legend.loc = "bottomright")
title(main = paste("Uncorrected Interbatch Distance:", round(huhnPCA, 3)))

huhnPCA.A <- evaluateCorrection(allResultsAve[["Q"]], set.3.Y, what = "PCA",
                                plot = TRUE, legend.loc = "bottomright")
title(main = paste("Corrected Interbatch Distance:", round(huhnPCA.A, 3)))

# huhnPCA.A <- evaluateCorrection(allResultsAve[["Q0"]], set.3.Y, what = "PCA",
#                                 plot = TRUE, legend.loc = "bottomright")
# title(main = paste("Q0: Interbatch distance:", round(huhnPCA.A, 3)))



results.ave <- results.line <- matrix(NA, length(experiments) + 1, 2)
dimnames(results.line) <- dimnames(results.ave) <-
  list(c("No correction", experiments), c("PCA", "duplo"))

results.line[1,1] <- results.ave[1,1] <-
  evaluateCorrection(set.3, set.3.Y, what = "PCA", plot = FALSE)
results.line[1,2] <- results.ave[1,2] <-
  evaluateCorrection(set.3, set.3.Y, what = "duplo", plot = FALSE)

for (exp in experiments[exp.idx]) {
  x <- allResultsAve[[exp]]
  woppa <- set.3
  woppa[!is.na(x)] <- x[!is.na(x)]
  results.ave[exp, 1] <-
    evaluateCorrection(woppa, set.3.Y, "PCA", plot = FALSE)
  results.ave[exp, 2] <-
    evaluateCorrection(woppa, set.3.Y, "duplo", plot = FALSE)
}

for (exp in experiments) {
  x <- allResultsLine[[exp]]
  woppa <- set.3
  woppa[!is.na(x)] <- x[!is.na(x)]
  results.line[exp, 1] <-
    evaluateCorrection(woppa, set.3.Y, "PCA", plot = FALSE)
  results.line[exp, 2] <-
    evaluateCorrection(woppa, set.3.Y, "duplo", plot = FALSE)
}

results.ruv <-
  cbind(sapply(allResultsRUV,
               evaluateCorrection, set.3.Y,
               what = "PCA", plot = FALSE),
        sapply(allResultsRUV,
               evaluateCorrection, set.3.Y,
               what = "duplo", plot = FALSE))
dimnames(results.ruv) <- list(paste("R", 0:2, sep = ""),
                              c("PCA", "duplo"))

# figure 6 
floodresults.ave <- rbind(results.ave, results.ruv)
floodresults.ave.label <- factor(substr(rownames(floodresults.ave), 1, 1))
floodresults.line <- rbind(results.line, results.ruv)
floodresults.line.label <- factor(substr(rownames(floodresults.line), 1, 1))
PCA.range <- range(c(floodresults.ave[,1], floodresults.line[,1]), 
                   na.rm = TRUE)
duplo.range <- range(c(floodresults.ave[,2], floodresults.line[,2]),
                     na.rm = TRUE)
par(mfrow = c(1,1))
plot(floodresults.ave[,1], floodresults.ave[,2],
     main = "Data set III - only batch correction",
     ylab= "Repeatability", xlab = "Interbatch distance",
     xlim = PCA.range, ylim = duplo.range, 
     col = as.integer(floodresults.ave.label))
text(floodresults.ave[,1], floodresults.ave[,2],
     pos = ifelse(floodresults.ave.label == "N", 2, 4),
     col = as.integer(floodresults.ave.label),
     labels = rownames(floodresults.ave))

plot(floodresults.line[,1], floodresults.line[,2], 
     main = "Data set III - batch and order correction", 
     xlim = PCA.range, ylim = duplo.range, 
     ylab= "Repeatability", xlab = "Interbatch distance",
     col = as.integer(floodresults.line.label))
text(floodresults.line[,1], floodresults.line[,2],
     pos = ifelse(floodresults.line.label %in% c("N", "Q"), 2, 4),
     col = as.integer(floodresults.line.label),
     labels = rownames(floodresults.line))


# log peak area mean
library("dplyr")
library("ggplot2")

raw <- data.frame(set.3)
#corrected <- data.frame(allResultsAve[["Q"]])
corrected <- data.frame(allResultsRUV[[0]])
row.names(corrected) <- row.names(raw)

raw[is.na(raw)] <- 0
corrected[is.na(corrected)] <- 0

raw['mean'] <- apply(raw, 1, mean)
corrected['mean'] <- apply(corrected, 1, mean)
raw_plus_meta <- merge(raw, set.3.Y, by="row.names", all=TRUE) 
corrected_plus_meta <- merge(corrected, set.3.Y, by="row.names", all=TRUE) 

plot_areas_batchwise<- function(df,title) {
  gm = mean(df$mean)
  ggplot() + 
    geom_point(data=df, mapping=aes(x=SeqNr, y=mean, color=Batch)) +
    xlab("injection order") + ylab("log mean peak area") + ggtitle(title) +
    geom_hline(yintercept=gm, linetype="dashed", color = "black") +
    stat_smooth(method="lm", formula=y~1, se=FALSE)
}

plot_areas_batchwise(raw_plus_meta,"Raw")
plot_areas_batchwise(corrected_plus_meta,"Corrected")

raw_refs <- raw_plus_meta[ which(raw_plus_meta$SCode=='ref'),]
raw_samples <- raw_plus_meta[ which(raw_plus_meta$SCode!='ref'),]
corrected_refs <- corrected_plus_meta[ which(corrected_plus_meta$SCode=='ref'),]
corrected_samples <- corrected_plus_meta[ which(corrected_plus_meta$SCode!='ref'),]

plot_areas_batchwise(raw_refs,"raw refs")
plot_areas_batchwise(corrected_refs,"corrected refs")
plot_areas_batchwise(raw_samples,"raw samples")
plot_areas_batchwise(corrected_samples,"corrected samples")



raw_plus_meta$Batch <- as.character(raw_plus_meta$Batch)
raw_plus_meta[ which(raw_plus_meta$SCode=='ref'),]$Batch = "QC"
raw_plus_meta$Batch <- as.factor(raw_plus_meta$Batch)

corrected_plus_meta$Batch <- as.character(corrected_plus_meta$Batch)
corrected_plus_meta[ which(corrected_plus_meta$SCode=='ref'),]$Batch = "QC"
corrected_plus_meta$Batch <- as.factor(corrected_plus_meta$Batch)

plot_areas_batchwise(raw_plus_meta,"raw")
plot_areas_batchwise(corrected_plus_meta,"corrected")


getPCA <- function(X, Y, GRAPH)
{			
  nbatches <- nlevels(Y$Batch)
  noref.idx <- which(Y$SCode != "ref")
  Xsample <- X[noref.idx,]
  YSample <- Y[noref.idx,]
  
  Xsample <- Xsample[, apply(Xsample, 2, function(x) !all(is.na(x)))]
  
  ## replace NA values with column means
  for (i in 1:ncol(Xsample))
    Xsample[is.na(Xsample[,i]),i] <- mean(Xsample[,i], na.rm = TRUE)
  
  Xsample <- Xsample[, apply(Xsample, 2, sd, na.rm = TRUE) > 0]
  ## Original is using ChemometricsWithR which reports an unintelligible result object, hence switching to something well maintained to get the PCA scores
  X.PCA <- FactoMineR::PCA(Xsample, scale.unit = TRUE, graph=GRAPH)
  
  return (X.PCA)
  
}



set3.uncorrected.PCA <- getPCA(set.3, set.3.Y,GRAPH = FALSE)
set3.uncorrected.PCAscores <- data.frame(set3.uncorrected.PCA$ind$coord)
set3.uncorrected.PCAscores <- merge(set3.uncorrected.PCAscores, set.3.Y, by="row.names", all=TRUE) 
write.csv(set3.uncorrected.PCAscores,"set3.uncorrected.PCA.csv", row.names = TRUE)

set3.corrected.PCA <- getPCA(corrected, set.3.Y,GRAPH = FALSE)
set3.corrected.PCAscores <- data.frame(set3.corrected.PCA$ind$coord)
set3.corrected.PCAscores <- merge(set3.corrected.PCAscores, set.3.Y, by="row.names", all=TRUE) 
write.csv(set3.corrected.PCAscores,"set3.corrected.PCA.csv", row.names = TRUE)


