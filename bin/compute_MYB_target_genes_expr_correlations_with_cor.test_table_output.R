args = commandArgs(trailingOnly=T)
expr_file = args[1]
outbase = args[2]
project = args[3]
corrGenes = args[4:length(args)]


iqr = function(values){return(IQR(values, na.rm=T))}
expr <- read.table(expr_file, header=T, sep="\t", row.names=1)
expr['iqr'] = apply(expr, 1, iqr)
expr = expr[expr$iqr > 0,]

corrGenes <- read.table(corrGenes)
rownames(corrGenes) <- corrGenes$V1
corrGenes <- intersect(rownames(corrGenes), rownames(expr)) 


set.seed(42)
cor = apply(apply(as.matrix(expr["MYB",]), 1, as.numeric), 2, function(x) {
     apply(as.matrix(expr[corrGenes,]), 1, function (y) {
         cor(x, as.numeric(y), use="na.or.complete", method="pearson")
     })
 })


cor.test_res <- cbind(apply(apply(as.matrix(expr["MYB",]), 1, as.numeric), 2, function(x) {
     apply(as.matrix(expr[corrGenes,]), 1, function (y) {
         cor.test(x, as.numeric(y), method="pearson")[["p.value"]]
     })
 }), apply(apply(as.matrix(expr["MYB",]), 1, as.numeric), 2, function(x) {
     apply(as.matrix(expr[corrGenes,]), 1, function (y) {
         cor.test(x, as.numeric(y), method="pearson" )[["estimate"]]
     })
 }))

colnames(cor.test_res) <- c("p-value", "estimate")
cor.test.vec <- as.data.frame(unlist(cor.test_res))
cor.test.vec$project <- project

write.table(cor.test.vec, paste0(outbase, "_", "cor.test_Targetgene_expr.vs.MYB.tsv"), quote =F, sep="\t", dec=".", row.names =T, col.names=NA)
write.table(cor, paste0(outbase, "_", "cor_Targetgene_expr.vs.MYB.tsv"), quote =F, sep="\t", dec=".", row.names =F)
