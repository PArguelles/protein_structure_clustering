

base_path_to_matrix <- "C:/ShareSSD/scop/data/values_"
base_path_to_result <- "C:/ShareSSD/scop/kde_"
base_path_to_stats <- 'C:/ShareSSD/scop/stats_'

sample = 'a.1.'
#measures = c('rmsd','gdt_2','gdt_4','tmscore_high','tmscore_low','maxsub_high','maxsub_low','seq_id') 
measures = c('rmsd','gdt_2','gdt_4','seq','tm','maxsub') 

for(measure in measures){

    path_to_matrix <- paste(base_path_to_matrix,'',sep='')
    path_to_matrix <- paste(path_to_matrix,sample,sep='')
    path_to_matrix <- paste(path_to_matrix,'_',sep='')
    path_to_matrix <- paste(path_to_matrix,measure,sep='')

    path_to_result <- paste(base_path_to_result,'',sep='')
    path_to_result <- paste(path_to_result,sample,sep='')
    path_to_result <- paste(path_to_result,'_',sep='')
    path_to_result <- paste(path_to_result,measure,sep='')
    path_to_result <- paste(path_to_result,'.jpg',sep='')

    path_to_stats <- paste(base_path_to_stats,'',sep='')
    path_to_stats <- paste(path_to_stats,sample,sep='')
    path_to_stats <- paste(path_to_stats,'_',sep='')
    path_to_stats <- paste(path_to_stats,measure,sep='')

    df <- read.table(path_to_matrix, header = FALSE)
    x <- df[,c(1)]
    names(x) <- c(measure)
    d <- density(x)

    jpeg(path_to_result)
    plot(d, main=measure)
    polygon(d,col='white',border='black')
    dev.off()

    mean <- 'Mean: '
    sd <- 'Standard deviation: '
    var <- 'Variance: ' 
    mean_value <- mean(x)
    sd_value <- sd(x)
    var_value <- var(x)

    mean <- paste(mean,mean_value,sep='')
    mean <- paste(mean,'\n',sep='')
    sd <- paste(sd,sd_value,sep='')
    sd <- paste(sd,'\n',sep='')
    var <- paste(var,var_value,sep='')
    var <- paste(var,'\n',sep='')

    sink(path_to_stats)
    cat(mean)
    cat(sd)
    cat(var)
    sink()

    path_to_matrix <- ''
    path_to_result <- ''
    path_to_stats <- ''

}
